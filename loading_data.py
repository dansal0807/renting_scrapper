#envio do dataset para o postgreslocalhost.
import pandas as pd
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import time
import sys

df = pd.read_csv('imoveis_dataset.csv',encoding='utf-8',sep=';')

def show_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()
    # get the line number when exception occured
    line_n = traceback.tb_lineno
    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

def execute_many(conn, datafrm, table):
    
    # Creating a list of tupples from the dataframe values
    tpls = [tuple(x) for x in datafrm.to_numpy()]
    
    # dataframe columns with Comma-separated
    cols = ','.join(list(datafrm.columns))
    
    # SQL query to execute
    sql = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s)" % (table, cols)
    cursor = conn.cursor()
    try:
        cursor.executemany(sql, tpls)
        conn.commit()
        print("Data inserted using execute_many() successfully...")
    except (Exception, psycopg2.DatabaseError) as err:
        # pass exception to function
        show_psycopg2_exception(err)
        cursor.close()

try:
    print('Connecting to the PostgreSQL...........')
    conn = psycopg2.connect(user="postgres",
                              password="***",
                              host="127.0.0.1",
                              port="5432",
                              database="postgres")
    print("Connection successful..................")
    conn.autocommit = True
    cursor = conn.cursor()


    create_table = """ CREATE TABLE IF NOT EXISTS rentings_rj 
                    (endereco VARCHAR(200),
                     valor VARCHAR(10),
                     area VARCHAR(10),
                     quartos VARCHAR(10),
                     vagas VARCHAR(10),
                     banheiros VARCHAR(10),
                     pagina VARCHAR(10))
                    """
    cursor.execute(create_table)
    conn.commit()
    
    tpls = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    table = 'rentings_rj'
    sql = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % (table, cols)

    print(df)
    cursor.executemany(sql,tpls)
    conn.commit()
    cursor.close()

except Exception as err:
        # passing exception to function
        print(err)
