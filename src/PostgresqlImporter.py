import psycopg2
import psycopg2.pool
import os
import time


def get_path(unzip_path, filename):
    """
    check the exact path of the target file
    :param unzip_path: the path of the zip file where it had been unziped
    :param filename: target filename
    :return:
    """
    if os.path.isdir(unzip_path + "/rrf"):
        file_dir = unzip_path + "/rrf/" + filename
    else:
        file_dir = unzip_path + "/" + filename
    return file_dir


def get_create_temp_table_sql(orig_table_name: str) -> str:
    """
    return the sql script to create a TEMPORARY TABLE which has the same structure of the given orig_table
    the TEMPORARY TABLE will be named with a prefix of "temp_"
    :param orig_table_name: str, the original table
    :return: the sql script
    """
    sql = "CREATE TEMPORARY TABLE temp_" + orig_table_name + " AS SELECT * FROM " + orig_table_name + " WHERE 1=0;"
    return sql


def get_update_date_sql(orig_table_name: str, unique_key_name: str) -> str:
    """
    return the sql script to update the last_update_file_date and create_file_date columns of the table
    :param orig_table_name: str, the name of the target table
    :param unique_key_name: str, the name of the unique_key used to decide whether a row is a duplicate record
    :return: the sql script
    """
    sql = "INSERT INTO " + orig_table_name + " SELECT * FROM temp_" + orig_table_name + " " \
          "ON CONFLICT ON CONSTRAINT " + unique_key_name + " DO UPDATE " \
          "SET last_update_file_date = " \
          "    CASE WHEN EXCLUDED.last_update_file_date > " + orig_table_name + ".last_update_file_date " \
          "         THEN EXCLUDED.last_update_file_date " \
          "         ELSE " + orig_table_name + ".last_update_file_date " \
          "    END, " \
          "    create_file_date = " \
          "    CASE WHEN EXCLUDED.create_file_date < " + orig_table_name + ".create_file_date" \
          "         THEN EXCLUDED.create_file_date " \
          "         ELSE " + orig_table_name + ".create_file_date " \
          "    END;"
    return sql


def get_copy_sql(orig_table_name: str, file_dir: str, field_list: str) -> str:
    """
    return the sql script to copy records from files into temp table
    :param orig_table_name: target table, without prefix of "temp_"
    :param file_dir: the target file path to import
    :param field_list: field lists to be imported into the table
    :return: the sql script
    """
    sql = "COPY temp_" + orig_table_name + "(" + \
          ','.join(field_list) + \
          ") FROM '" + file_dir + "' DELIMITER '|' QUOTE '$' CSV;"
    return sql


def get_update_temp_date_sql(orig_table_name: str, date: str) -> str:
    """
    return the sql script to update create_file_date and last_update_file_date in the temp_target_table with given date
    :param orig_table_name: str, target table without prefix of "temp_"
    :param date: str,'YYYY-mm-dd' given date to update the fields, should corresponding to the date the file released
    :return: the sql script
    """
    sql = "UPDATE temp_" + orig_table_name + \
          " SET create_file_date='" + date + "',last_update_file_date='" + date + "'; "
    return sql


def get_drop_temp_table_sql(orig_table_name: str) -> str:
    """
    return the sql script to drop the temp table
    :param orig_table_name: str, target table without prefix of "temp_"
    :return: the sql script
    """
    sql = "DROP TABLE temp_" + orig_table_name + ";"
    return sql


class PostgresqlImporter:
    def __init__(self, user, password, database, host='localhost', port=5432, target_schema="public"):
        """
        init the db connection
        :param user: username of your database used to authenticate
        :param password: password used to authenticate
        :param database: target database name that your want the rxnorm rrf files to be imported into
        :param host: database host address (defaults to UNIX socket if not provided)
        :param port: connection port number (defaults to 5432 if not provided)
        """
        self.pool = psycopg2.pool.ThreadedConnectionPool(minconn=1, maxconn=25,
                                                         user=user, password=password, database=database,
                                                         host=host, port=port,
                                                         options="-c search_path=" + target_schema,
                                                         )

    def close_all(self):
        self.pool.closeall()

    def execute_sql_list_with_op(self, sql_op_list: list) -> str:
        """
        execute the sql script given by the list, in the field of "sql"
        and the field og "op" give the additional operations by the key of the dict and the name to log this op
        'T' means log the Time used, 'RC' means log the row counts that had been affected
        op_list_example = [
            {'sql': sql_create_temp_table},
            {'sql': sql_copy , 'op':{'T':"Import Time",'RC':'Records'}},
            {'sql': sql_update_temp},
            {'sql': sql_update_orig, 'op':{'T':"Update Time",'RC':'Records Updated'}},
            {'sql': sql_drop_temp_table},
        ]
        :param sql_op_list: a list of dict with the keys of 'sql' and 'op'(not required)
        :return:str, the log
        """
        conn = self.pool.getconn()
        cursor = conn.cursor()
        cursor.execute("SET client_encoding = 'utf8'")
        log = ''
        for current_op in sql_op_list:
            sql = current_op.get("sql")
            op = current_op.get("op")
            if op is not None and 'T' in op.keys():
                # Need Timing
                time1 = time.time()
            cursor.execute(sql)
            if op is not None and 'T' in op.keys():
                time2 = time.time()
                log = log + op.get('T') + ": " + "{:.2f}s".format(time2 - time1) + "; "
            if op is not None and 'RC' in op.keys():
                rc = cursor.rowcount
                log = log + op.get('RC') + ": " + str(rc) + "; "
        conn.commit()
        self.pool.putconn(conn)
        return log

    def import_rxnconso(self, file_form):
        """
        Load RXNCONSO.rrf into schema
        :param file_form:
        :return:
        """
        # construct SQL script
        date = file_form.get('date')
        file_dir = get_path(file_form.get('unzip_dir'), "RXNCONSO.RRF")
        # Deal with RxNorm_2005-05-06 has a extra '|' at the end of each line
        if date == '2005-05-06':
            sql_copy = get_copy_sql(orig_table_name='rxnconso', file_dir=file_dir, field_list=[
                '\"RXCUI\"', '\"LAT\"', '\"TS\"', '\"LUI\"', '\"STT\"', '\"SUI\"', '\"ISPREF\"', '\"RXAUI\"',
                '\"SAUI\"', '\"SCUI\"', '\"SDUI\"', '\"SAB\"', '\"TTY\"', '\"CODE\"', '\"STR\"', '\"SRL\"',
                '\"SUPPRESS\"', '\"CVF\"', 'create_file_date', 'last_update_file_date'
            ])
        else:
            sql_copy = get_copy_sql(orig_table_name='rxnconso', file_dir=file_dir, field_list=[
                '\"RXCUI\"', '\"LAT\"', '\"TS\"', '\"LUI\"', '\"STT\"', '\"SUI\"', '\"ISPREF\"', '\"RXAUI\"',
                '\"SAUI\"', '\"SCUI\"', '\"SDUI\"', '\"SAB\"', '\"TTY\"', '\"CODE\"', '\"STR\"', '\"SRL\"',
                '\"SUPPRESS\"', '\"CVF\"', 'create_file_date'
            ])
        sql_update_temp = get_update_temp_date_sql(orig_table_name="rxnconso", date=date)
        sql_update_orig = get_update_date_sql(orig_table_name="rxnconso", unique_key_name="uk_rxnconso")
        sql_create_temp_table = get_create_temp_table_sql(orig_table_name="rxnconso")
        sql_drop_temp_table = get_drop_temp_table_sql(orig_table_name="rxnconso")
        # execute sql script
        # Deal with SUPPRESS VARCHAR(8) changed to VARCHAR(1) since 2006-06-05,
        # and announced in release of 2005-07-29 that 'Obsolete' changed to 'O'
        if date < '2005-07-29':
            sql_alter_temp = "ALTER TABLE temp_rxnconso ALTER COLUMN \"SUPPRESS\" TYPE character varying(8);"
            sql_update_temp_fields = "UPDATE temp_rxnconso SET \"SUPPRESS\"='O' WHERE \"SUPPRESS\"='Obsolete';"
            sql_alter_temp_back = "ALTER TABLE temp_rxnconso ALTER COLUMN \"SUPPRESS\" TYPE character varying(1);"
            sql_op_list = [
                {'sql': sql_create_temp_table},
                {'sql': sql_alter_temp},
                {'sql': sql_copy, 'op': {'T': "Import Time", 'RC': 'Records'}},
                {'sql': sql_update_temp},
                {'sql': sql_update_temp_fields},
                {'sql': sql_alter_temp_back},
                {'sql': sql_update_orig, 'op': {'T': "Update Time", 'RC': 'Records Updated'}},
                {'sql': sql_drop_temp_table},
            ]
        else:
            sql_op_list = [
                {'sql': sql_create_temp_table},
                {'sql': sql_copy, 'op': {'T': "Import Time", 'RC': 'Records'}},
                {'sql': sql_update_temp},
                {'sql': sql_update_orig, 'op': {'T': "Update Time", 'RC': 'Records Updated'}},
                {'sql': sql_drop_temp_table},
            ]
        log = self.execute_sql_list_with_op(sql_op_list)
        print("RXNCONSO: " + log)

    def import_rxnrel(self, file_form):
        """ Load RXNREL.rrf into schema"""
        # construct SQL script
        date = file_form.get('date')
        file_dir = get_path(file_form.get('unzip_dir'), "RXNREL.RRF")
        sql_copy = get_copy_sql(orig_table_name='rxnrel', file_dir=file_dir, field_list=[
            '\"RXCUI1\"', '\"RXAUI1\"', '\"STYPE1\"', '\"REL\"', '\"RXCUI2\"', '\"RXAUI2\"', '\"STYPE2\"', '\"RELA\"',
            '\"RUI\"', '\"SRUI\"', '\"SAB\"', '\"SL\"', '\"DIR\"', '\"RG\"', '\"SUPPRESS\"', '\"CVF\"',
            'create_file_date'
        ])
        sql_create_temp_table = get_create_temp_table_sql(orig_table_name="rxnrel")
        sql_drop_temp_table = get_drop_temp_table_sql(orig_table_name="rxnrel")
        sql_update_temp = get_update_temp_date_sql(orig_table_name="rxnrel", date=date)
        sql_update_orig = get_update_date_sql(orig_table_name="rxnrel", unique_key_name="uk_rxnrel")
        # execute sql script
        sql_op_list = [
            {'sql': sql_create_temp_table},
            {'sql': sql_copy, 'op': {'T': "Import Time", 'RC': 'Records'}},
            {'sql': sql_update_temp},
            {'sql': sql_update_orig, 'op': {'T': "Update Time", 'RC': 'Records Updated'}},
            {'sql': sql_drop_temp_table},
        ]
        log = self.execute_sql_list_with_op(sql_op_list)
        print("RXNREL: " + log)

    def import_rxnsat(self, file_form):
        """ Load RXNSAT.rrf into schema"""
        # construct SQL script
        date = file_form.get('date')
        file_dir = get_path(file_form.get('unzip_dir'), "RXNSAT.RRF")
        # Deal with RxNorm_2005-05-06 has an extra '|' at the end of each line
        if date == '2005-05-06':
            sql_copy = "COPY temp_rxnsat(\"RXCUI\",\"LUI\",\"SUI\",\"RXAUI\",\"STYPE\",\"CODE\",\"ATUI\",\"SATUI\"," \
                       "\"ATN\",\"SAB\",\"ATV\",\"SUPPRESS\",\"CVF\",create_file_date,last_update_file_date) FROM '" \
                       + file_dir + "' DELIMITER '|' QUOTE '$' CSV; "
        else:
            sql_copy = "COPY temp_rxnsat(\"RXCUI\",\"LUI\",\"SUI\",\"RXAUI\",\"STYPE\",\"CODE\",\"ATUI\",\"SATUI\"," \
                       "\"ATN\",\"SAB\",\"ATV\",\"SUPPRESS\",\"CVF\",create_file_date) FROM '" \
                       + file_dir + "' DELIMITER '|' QUOTE '$' CSV; "
        sql_update_temp = get_update_temp_date_sql(orig_table_name="rxnsat", date=date)
        sql_update_orig = get_update_date_sql(orig_table_name="rxnsat", unique_key_name="uk_rxnsat")
        sql_delete_duplicate_rows = \
            "DELETE FROM temp_rxnsat WHERE ctid IN ( " \
            "    SELECT ctid FROM ( " \
            "        SELECT ctid,\"RXCUI\",\"LUI\",\"SUI\",\"RXAUI\",\"STYPE\",\"CODE\",\"ATUI\",\"SATUI\",\"ATN\"," \
            "               \"SAB\",\"ATV\",\"SUPPRESS\",\"CVF\"," \
            "               row_number() over (PARTITION BY \"RXCUI\",\"LUI\",\"SUI\",\"RXAUI\",\"STYPE\",\"CODE\"," \
            "                   \"ATUI\",\"SATUI\",\"ATN\",\"SAB\",\"ATV\",\"SUPPRESS\",\"CVF\" ORDER BY ctid) " \
            "               AS row_num FROM temp_rxnsat) AS d WHERE row_num > 1 );"
        sql_create_temp_table = get_create_temp_table_sql(orig_table_name="rxnsat");
        sql_drop_temp_table = get_drop_temp_table_sql(orig_table_name="rxnsat")
        # execute sql script
        sql_op_list = [
            {'sql': sql_create_temp_table},
            {'sql': sql_copy, 'op': {'T': "Import Time", 'RC': 'Records'}},
            {'sql': sql_delete_duplicate_rows},
            {'sql': sql_update_temp},
            {'sql': sql_update_orig, 'op': {'T': "Update Time", 'RC': 'Records Updated'}},
            {'sql': sql_drop_temp_table},
        ]
        log = self.execute_sql_list_with_op(sql_op_list)
        print("RXNSAT: " + log)

    def import_rxnsty(self, fileform):
        """ Load RXNSTY.rrf into schema"""
        # construct SQL script
        date = fileform.get('date')
        file_dir = get_path(fileform.get('unzip_dir'), "RXNSTY.RRF")
        # Deal with RxNorm_2005-05-06 has a extra '|' at the end of each line
        if date == '2005-05-06':
            sql_copy = "COPY temp_rxnsty(\"RXCUI\",\"TUI\",\"STN\",\"STY\",\"ATUI\",\"CVF\",create_file_date," \
                       "last_update_file_date) FROM '" + file_dir + "' DELIMITER '|' QUOTE '$' CSV;"
        else:
            sql_copy = "COPY temp_rxnsty(\"RXCUI\",\"TUI\",\"STN\",\"STY\",\"ATUI\",\"CVF\",create_file_date)" \
                       "FROM '" + file_dir + "' DELIMITER '|' QUOTE '$' CSV;"
        sql_update_temp = get_update_temp_date_sql(orig_table_name="rxnsty", date=date)
        sql_update_orig = get_update_date_sql(orig_table_name="rxnsty", unique_key_name="uk_rxnsty")
        sql_delete_duplicate_rows = "DELETE FROM temp_rxnsty WHERE ctid IN ( " \
                                    "   SELECT ctid FROM (" \
                                    "       SELECT ctid,\"RXCUI\",\"TUI\",\"STN\",\"STY\",\"ATUI\",\"CVF\"," \
                                    "       row_number() over (PARTITION BY \"RXCUI\",\"TUI\",\"STN\",\"STY\"," \
                                    "           \"ATUI\",\"CVF\" ORDER BY ctid ASC) AS row_num " \
                                    "   FROM temp_rxnsty) AS d" \
                                    "   WHERE row_num > 1" \
                                    ")"
        sql_create_temp_table = get_create_temp_table_sql(orig_table_name="rxnsty")
        sql_drop_temp_table = get_drop_temp_table_sql(orig_table_name="rxnsty")
        # execute sql script
        sql_op_list = [
            {'sql': sql_create_temp_table},
            {'sql': sql_copy, 'op': {'T': "Import Time", 'RC': 'Records'}},
            {'sql': sql_delete_duplicate_rows},
            {'sql': sql_update_temp},
            {'sql': sql_update_orig, 'op': {'T': "Update Time", 'RC': 'Records Updated'}},
            {'sql': sql_drop_temp_table},
        ]
        log = self.execute_sql_list_with_op(sql_op_list)
        print("RXNSTY: " + log)

    def import_rxncuichanges(self, file_form):
        """ Load RXNCUICHANGES.rrf into schema"""
        # construct SQL script
        date = file_form.get('date')
        file_dir = get_path(file_form.get('unzip_dir'), "RXNCUICHANGES.RRF")
        if not os.path.exists(file_dir):
            return "[WARN] File RXNCUICHANGES.RRF Not exist!"
        sql_copy = "COPY temp_rxncuichanges(\"RXAUI\",\"CODE\",\"SAB\",\"TTY\",\"STR\",\"OLD_RXCUI\",\"NEW_RXCUI\"," \
                   "create_file_date) FROM '" + file_dir + "' DELIMITER '|' QUOTE '$' CSV; "
        sql_update_temp = get_update_temp_date_sql(orig_table_name="rxncuichanges", date=date)
        sql_update_orig = get_update_date_sql(orig_table_name="rxncuichanges", unique_key_name="uk_rxncuichanges")
        sql_create_temp_table = get_create_temp_table_sql(orig_table_name="rxncuichanges")
        sql_drop_temp_table = get_drop_temp_table_sql(orig_table_name="rxncuichanges")
        # execute sql script
        sql_op_list = [
            {'sql': sql_create_temp_table},
            {'sql': sql_copy, 'op': {'T': "Import Time", 'RC': 'Records'}},
            {'sql': sql_update_temp},
            {'sql': sql_update_orig, 'op': {'T': "Update Time", 'RC': 'Records Updated'}},
            {'sql': sql_drop_temp_table},
        ]
        log = self.execute_sql_list_with_op(sql_op_list)
        print("RXNCUICHANGES: " + log)
