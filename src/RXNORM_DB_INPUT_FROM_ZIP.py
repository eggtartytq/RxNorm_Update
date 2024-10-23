import os
import settings
import zipfile
import time
import shutil
import threading


def get_importer(dbms):
    """
    Get the importer for target DBMS.
    This importer includes Database connection pool and all the methods to import all supported tables
    :param dbms:
    :return:
    """
    if dbms == 'mysql':
        from MysqlImporter import MysqlImporter
        dbImporter = MysqlImporter(user=settings.DB_USER, password=settings.DB_PASSWORD,
                                   database=settings.DB_DATABASE,
                                   host=settings.DB_HOST, port=settings.DB_PORT)
    elif dbms == 'postgresql':
        from PostgresqlImporter import PostgresqlImporter
        dbImporter = PostgresqlImporter(user=settings.DB_USER, password=settings.DB_PASSWORD,
                                        database=settings.DB_DATABASE,
                                        host=settings.DB_HOST, port=settings.DB_PORT,
                                        target_schema=settings.DB_TARGET_SCHEMA)
    else:
        raise ValueError('Unexpected DBMS name')
    return dbImporter


def unzip_file(file_name, unzip_dir):
    """
    zip files unzip to folder with folder name subfix='_files'
    :param unzip_dir:
    :param file_name:
    :return: unzip_dir, folder path of the unzipped file
    """
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(unzip_dir):
        pass
    else:
        os.mkdir(unzip_dir)
    zip_file.extractall(unzip_dir)
    return unzip_dir


def unzip_file_thread(filename, unzip_dir):
    """
    Use a thread to execute unzip process, so can wait until unzip done
    :param filename: target file to uznip
    :param unzip_dir: target path to store unzipped files
    :return:
    """
    # Create a thread for the extraction
    extraction_thread = threading.Thread(target=unzip_file, args=(filename, unzip_dir))
    # Start the extraction thread
    extraction_thread.start()
    # Wait for the extraction thread to finish
    extraction_thread.join()


def get_expression_and_param(selected_table_set):
    """
    Construct expression and parameters for parallel execution.
    :param selected_table_set: Tables selected to be import
    :return: expr_with_param, a list of (expr, param) tuples
    """
    expr_with_param = []
    # A dict giving corresponding methods for each table
    TABLE_IMPORT_FUNC_NAME_DICT = {
        'RXNCONSO': 'import_rxnconso',
        'RXNSAT': 'import_rxnsat',
        'RXNSTY': 'import_rxnsty',
        'RXNREL': 'import_rxnrel',
        'RXNCUICHANGES': 'import_rxncuichanges'
    }
    for testTableName in TABLE_IMPORT_FUNC_NAME_DICT.keys():
        if testTableName in selected_table_set:
            expr = "dbImporter.{}".format(TABLE_IMPORT_FUNC_NAME_DICT.get(testTableName))
            param = fileForm.loc[i]
            expr_with_param.append((expr, param))
    return expr_with_param


def evaluate_expression(expr, param):
    """
    Evaluate Expression with parameters
    :param expr:
    :param param:
    :return:
    """
    try:
        eval(expr)(param)
    except Exception as e:
        print(e)


def exec_expression_in_parallel(expr_with_param):
    """
    Parallelly execute expressions with parameters given by expr_with_param
    :param expr_with_param:  a list of (expr, param) tuples
    :return:
    """
    # Create and start a thread for each expression
    threads = []
    time_start = time.time()
    for expr, param in expr_with_param:
        thread = threading.Thread(target=evaluate_expression, args=(expr, param))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    time_end = time.time()

    print("Process Finished: " + fileForm.loc[i, 'date'] + " Total Time:{:.2f}s".format(time_end - time_start))


if __name__ == '__main__':
    from GetConfig import get_config

    # fileform： a dataframe with target zip file ['file', 'date', 'unzip_dir'] to import
    dbms, selected_table_set, fileForm = get_config()
    dbImporter = get_importer(dbms)

    for i in fileForm.index:
        # unzip file to corresponding path
        print("Processing: " + fileForm.loc[i, 'date'])
        filename = fileForm.loc[i, 'file']
        un_zip_dir = filename.split(".")[0] + "_files"
        unzip_file_thread(filename, un_zip_dir)
        fileForm.loc[i, 'unzip_dir'] = un_zip_dir
        # import rrf into DB in parallel
        expr_with_param = get_expression_and_param(selected_table_set)
        exec_expression_in_parallel(expr_with_param)
        # delete unzipped folder/files
        shutil.rmtree(fileForm.loc[i, 'unzip_dir'])
    dbImporter.close_all()
