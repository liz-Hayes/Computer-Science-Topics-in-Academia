import mysql.connector
import pandas as pd

USERNAME="root"
PASSWORD= "test_root"
HOST = '127.0.0.1'
DATABASE = "academicworld"

CONFIG = {
    "host": HOST,
    "user": USERNAME,
    "password": PASSWORD,
    "database": DATABASE
}


def connect(config=CONFIG):
    try:
        return mysql.connector.connect(**config)
    except (mysql.connector.Error, IOError) as err:
        print(err)
    return None

def query(query,config=CONFIG):
    cnx = connect(config=config)
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            cursor.execute(query)
            col_names = [ x[0] for x in cursor.description]
            out =  cursor.fetchall()
            df = pd.DataFrame(out, columns=col_names)
        cnx.close()
    return df

def insert(insert_cols, insert_vals,config=CONFIG):
    cnx = connect(config=config)
    if cnx and cnx.is_connected():
        #PREPARED STATEMENT
        with cnx.cursor(prepared=True) as cursor:
            #SQL TRANSACTIONS
            try:
                #
                cursor.execute(insert_cols, insert_vals)
                cnx.commit()
            except:
                cnx.rollback()
        cnx.close()
def exec(stmnt,config=CONFIG):
    cnx = connect(config=config)
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:
            #SQL TRANSACTIONS
            try:
                cursor.execute(stmnt)
                cnx.commit()
            except:
                cnx.rollback()
        cnx.close()

def delete(delete_stmnt,config=CONFIG):
    cnx = connect(config=config)
    if cnx and cnx.is_connected():
        #SQL TRANSACTIONS
        with cnx.cursor() as cursor:
            try:
                cursor.execute(delete_stmnt)
                cnx.commit()
            except:
                cnx.rollback()
        cnx.close()
