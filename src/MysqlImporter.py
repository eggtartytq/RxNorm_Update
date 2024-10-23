import pymysqlpool
import os
import time


def get_path(unzip_path, filename):
    """
    check the exact path of the target file
    :param unzip_path: the path of the zip file where it had been unzipped
    :param filename: target filename
    :return:
    """
    if os.path.isdir(unzip_path + "/rrf"):
        file_dir = unzip_path + "/rrf/" + filename
    else:
        file_dir = unzip_path + "/" + filename
    return file_dir


class MysqlImporter:
    def __init__(self, user=None, password='', database=None, host='localhost', port=3306):
        """
        init the db connection
        :param user: username of your database used to authenticate
        :param password: password used to authenticate
        :param database: target database name that your want the RXNORM rrf files to be imported into
        :param host: database host address
        :param port: connection port number
        """
        self.pool = pymysqlpool.ConnectionPool(size=3, maxsize=9, pre_create_num=3, con_lifetime=0, name='mysql_pool',
                                               user=user, passwd=password, db=database,
                                               host=host, port=port,
                                               local_infile=1)

    def close_all(self):
        pass

    def import_rxnconso(self, fileform):
        """ Load RXNCONSO.rrf into schema"""
        # construct SQL script
        date = fileform.get('date')
        file_dir = get_path(fileform.get('unzip_dir'), "RXNCONSO.RRF")
        sql_script1 = "load data local infile '" + file_dir + "' " \
                     "into table temp_RXNCONSO fields terminated by '|' ESCAPED BY '?'  lines terminated by '\\n' " \
                     "(@rxcui, @lat, @ts, @lui, @stt, @sui, @ispref, @rxaui, @saui, @scui, @sdui, @sab, @tty, @code, @str, @srl, @suppress, @cvf) " \
                     "SET rxcui =@rxcui, lat =@lat, ts =@ts, lui =@lui, stt =@stt, sui =@sui, ispref =@ispref, rxaui =@rxaui, saui =@saui, scui =@scui, " \
                     "sdui =@sdui, sab =@sab, tty =@tty, code =@code, str =@str, srl =@srl, suppress=@suppress, cvf=@cvf, " \
                     "create_file_date = '" + date + "', " \
                     "last_update_file_date = '" + date + "';"
        sql_script2 ="INSERT INTO rxnconso (rxcui, lat, ts, lui, stt, sui, ispref, rxaui, saui, scui, sdui, sab, tty, "\
                     "code, str, srl, suppress, cvf, STR_MD5,create_file_date,last_update_file_date)" \
                     "SELECT rxcui, lat, ts, lui, stt, sui, ispref, rxaui, saui, scui, sdui, sab, tty, code, str, " \
                     "srl, suppress, cvf, STR_MD5, create_file_date,last_update_file_date FROM temp_RXNCONSO " \
                     "ON DUPLICATE KEY UPDATE rxnconso.last_update_file_date=IF('" + date + "'>rxnconso.last_update_file_date,'" + date + "',rxnconso.last_update_file_date)," \
                                                                                                                                          "rxnconso.create_file_date=IF('" + date + "'<rxnconso.create_file_date,'" + date + "',rxnconso.create_file_date);"
        # execute sql script
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SET character_set_connection = utf8")
        cursor.execute("CREATE TEMPORARY TABLE temp_RXNCONSO SELECT * FROM  RXNCONSO WHERE 1=0;")
        time1 = time.time()
        a = cursor.execute(sql_script1)
        time2 = time.time()
        cursor.execute("UPDATE temp_RXNCONSO SET STR_MD5 = MD5(STR);")
        time3 = time.time()
        b = cursor.execute(sql_script2)
        time4 = time.time()
        cursor.execute("DROP TEMPORARY TABLE temp_RXNCONSO;")
        conn.commit()
        conn.close()
        print("RXNCONSO " + date + ": Records: " + str(a) + "; Records Updated: " + str(
            b) + "; Import time: {:.2f}s".format(
            time2 - time1) + "; MD5 time: {:.2f}s".format(time3 - time2) + "; Update time: {:.2f}s".format(
            time4 - time3))

    def import_rxnrel(self, fileform):
        """ Load RXNREL.rrf into schema"""
        # construct SQL script
        date = fileform.get('date')
        file_dir = get_path(fileform.get('unzip_dir'), "RXNREL.RRF")
        sql_script1 = "load data local infile '" + file_dir + "' " \
                     "into table temp_rxnrel fields terminated by '|' ESCAPED BY '?'  lines terminated by '\\n' " \
                     "(@rxcui1, @rxaui1, @stype1, @rel, @rxcui2, @rxaui2, @stype2, @rela, @rui, @srui, @sab, @sl, @rg, @dir, @suppress, @cvf)" \
                     "SET rxcui1 =@rxcui1, rxaui1 =@rxaui1, stype1 =@stype1, rel =@rel, rxcui2 =@rxcui2, rxaui2 =@rxaui2, stype2 =@stype2, " \
                     "rela =@rela, rui=@rui, srui=@srui, sab =@sab, sl =@sl, rg=@rg, dir=@dir, suppress=@suppress, cvf=@cvf," \
                     "create_file_date = '" + date + "', " \
                     "last_update_file_date = '" + date + "';"
        sql_script2 = "INSERT INTO rxnrel " \
                     "SELECT * FROM temp_rxnrel " \
                     "ON DUPLICATE KEY UPDATE rxnrel.last_update_file_date=IF('" + date + "'>rxnrel.last_update_file_date,'" + date + "',rxnrel.last_update_file_date)," \
                                                                                                                                      "rxnrel.create_file_date=IF('" + date + "'<rxnrel.create_file_date,'" + date + "',rxnrel.create_file_date);"
        # execute sql script
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SET character_set_connection = utf8")
        cursor.execute("CREATE TEMPORARY TABLE temp_RXNREL SELECT * FROM RXNREL WHERE 1=0")
        time1 = time.time()
        a = cursor.execute(sql_script1)
        time2 = time.time()
        cursor.execute("UPDATE temp_rxnrel SET SL_MD5 = MD5(SL);")
        time3 = time.time()
        b = cursor.execute(sql_script2)
        time4 = time.time()
        cursor.execute("DROP TEMPORARY TABLE temp_rxnrel;")
        conn.commit()
        conn.cursor()
        print("RXNREL " + date + ": Records: " + str(a) + "; Records Updated: " + str(
            b) + "; Import time: {:.2f}s".format(
            time2 - time1) + "; MD5 time: {:.2f}s".format(time3 - time2) + "; Update time: {:.2f}s".format(
            time4 - time3))

    def import_rxnsat(self, fileform):
        """ Load RXNSAT.rrf into schema"""
        # construct SQL script
        date = fileform.get('date')
        file_dir = get_path(fileform.get('unzip_dir'), "RXNSAT.RRF")
        sql_script1 = "load data local infile '" + file_dir + "' " \
                     "into table temp_rxnsat fields terminated by '|' ESCAPED BY '?'  lines terminated by '\\n' " \
                     "(@RXCUI,  @LUI,   @SUI,   @RXAUI, @STYPE, @CODE, " \
                     "@ATUI,    @SATUI, @ATN,   @SAB,   @ATV,   @SUPPRESS,  @CVF)" \
                     "SET RXCUI =@RXCUI,    LUI =@LUI,  SUI =@SUI,  RXAUI =@RXAUI,  STYPE =@STYPE,  CODE =@CODE," \
                     "ATUI =@ATUI,      SATUI =@SATUI, ATN=@ATN, SAB=@SAB, ATV =@ATV, SUPPRESS =@SUPPRESS, CVF=@CVF," \
                     "create_file_date = '" + date + "', " \
                     "last_update_file_date = '" + date + "';"
        sql_script2 = "INSERT INTO rxnsat " \
                     "SELECT * FROM temp_rxnsat " \
                     "ON DUPLICATE KEY UPDATE rxnsat.last_update_file_date=IF('" + date + "'>rxnsat.last_update_file_date,'" + date + "',rxnsat.last_update_file_date)," \
                                                                                                                                      "rxnsat.create_file_date=IF('" + date + "'<rxnsat.create_file_date,'" + date + "',rxnsat.create_file_date);"
        # execute sql script
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SET character_set_connection = utf8")
        cursor.execute("CREATE TEMPORARY TABLE temp_RXNSAT SELECT * FROM RXNSAT WHERE 1=0;")
        time1 = time.time()
        a = cursor.execute(sql_script1)
        time2 = time.time()
        cursor.execute("UPDATE temp_RXNSAT SET ATN_MD5 = MD5(ATN), ATV_MD5=MD5(ATV);")
        time3 = time.time()
        b = cursor.execute(sql_script2)
        time4 = time.time()
        cursor.execute("DROP TEMPORARY TABLE temp_RXNSAT;")
        conn.commit()
        conn.close()
        print("RXNSAT " + date + ": Records: " + str(a) + "; Records Updated: " + str(
            b) + "; Import time: {:.2f}s".format(
            time2 - time1) + "; MD5 time: {:.2f}s".format(time3 - time2) + "; Update time: {:.2f}s".format(
            time4 - time3))

    def import_rxnsty(self, fileform):
        """ Load RXNSTY.rrf into schema"""
        # construct SQL script
        date = fileform.get('date')
        file_dir = get_path(fileform.get('unzip_dir'), "RXNSTY.RRF")
        sql_script1 = "load data local infile '" + file_dir + "' " \
                     "into table temp_RXNSTY fields terminated by '|' ESCAPED BY '?'  lines terminated by '\\n' " \
                     "(@RXCUI, @TUI, @STN, @STY, @ATUI, @CVF)" \
                     "SET RXCUI =@RXCUI, TUI =@TUI, STN =@STN, STY =@STY, ATUI =@ATUI, CVF =@CVF, " \
                     "create_file_date = '" + date + "', " \
                     "last_update_file_date = '" + date + "';"
        sql_script2 = "INSERT INTO RXNSTY " \
                     "SELECT * FROM temp_RXNSTY " \
                     "ON DUPLICATE KEY UPDATE RXNSTY.last_update_file_date=IF('" + date + "'>RXNSTY.last_update_file_date,'" + date + "',RXNSTY.last_update_file_date)," \
                                                                                                                                      "RXNSTY.create_file_date=IF('" + date + "'<RXNSTY.create_file_date,'" + date + "',RXNSTY.create_file_date);"
        # execute sql script
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SET character_set_connection = utf8")
        cursor.execute("CREATE TEMPORARY TABLE temp_RXNSTY SELECT * FROM RXNSTY WHERE 1=0")
        time1 = time.time()
        a = cursor.execute(sql_script1)
        time2 = time.time()
        b = cursor.execute(sql_script2)
        time3 = time.time()
        cursor.execute("DROP TEMPORARY TABLE temp_RXNSTY;")
        conn.commit()
        conn.close()
        print("RXNSTY " + date + ": Records: " + str(a) + "; Records Updated: " + str(
            b) + "; Import time: {:.2f}s".format(
            time2 - time1) + "; Update time: {:.2f}s".format(time3 - time2))

    def import_rxncuichanges(self, fileform):
        """ Load RXNCUICHANGES.rrf into schema"""
        # construct SQL script
        date = fileform.get('date')
        file_dir = get_path(fileform.get('unzip_dir'), "RXNCUICHANGES.RRF")
        if not os.path.exists(file_dir):
            return "[WARN] File RXNCUICHANGES.RRF Not exist!"
        sql_script1 = "load data local infile '" + file_dir + "' " \
                     "into table temp_RXNCUICHANGES fields terminated by '|' ESCAPED BY '?' lines terminated by '\\n' "\
                     "(@RXAUI,  @CODE,   @SAB,   @TTY, @STR, @OLD_RXCUI, @NEW_RXCUI) " \
                     "SET RXAUI =@RXAUI,CODE =@CODE,  SAB =@SAB,  TTY =@TTY," \
                     "STR =@STR,    OLD_RXCUI=@OLD_RXCUI," \
                     "NEW_RXCUI =@NEW_RXCUI," \
                     "create_file_date = '" + date + "', " \
                     "last_update_file_date = '" + date + "';"
        sql_script2 = "INSERT INTO RXNCUICHANGES  SELECT * FROM temp_RXNCUICHANGES " \
                     "ON DUPLICATE KEY UPDATE RXNCUICHANGES.last_update_file_date=IF('" + date + "'>RXNCUICHANGES.last_update_file_date,'" + date + "',RXNCUICHANGES.last_update_file_date)," \
                                                                                                                                                    "RXNCUICHANGES.create_file_date=IF('" + date + "'<RXNCUICHANGES.create_file_date,'" + date + "',RXNCUICHANGES.create_file_date);"
        # execute sql script
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SET character_set_connection = utf8")
        cursor.execute("CREATE TEMPORARY TABLE temp_RXNCUICHANGES SELECT * FROM RXNCUICHANGES WHERE 1=0;")
        time1 = time.time()
        a = cursor.execute(sql_script1)
        time2 = time.time()
        cursor.execute("UPDATE temp_RXNCUICHANGES SET STR_MD5 = MD5(STR);")
        time3 = time.time()
        b = cursor.execute(sql_script2)
        time4 = time.time()
        cursor.execute("DROP TEMPORARY TABLE temp_RXNCUICHANGES;")
        conn.commit()
        conn.close()
        print("RXNCUICHANGES " + date + ": Records: " + str(a) + "; Records Updated: " + str(
            b) + "; Import time: {:.2f}s".format(
            time2 - time1) + "; MD5 time: {:.2f}s".format(time3 - time2) + "; Update time: {:.2f}s".format(
            time4 - time3))
