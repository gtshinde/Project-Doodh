import os
import psycopg2

def connect():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user='postgres',
        password='postgres')

    # Open a cursor to perform database operations
    # cur = conn.cursor()
    # sqlTxt='SELECT Item_Type FROM ITEMS'
    # cur.execute(sqlTxt)
    # # print(cur.execute(sqlTxt))
    # item_name = cur.fetchone()
    # cur.close()
    # conn.close()
    # return item_name
    
    return conn

def insert_into_items(item_type, item_price):
    conn = connect()
    cur = conn.cursor()
    sql_txt="""INSERT INTO ITEMS (Item_ID,Item_Type,Price, created_date, last_updated_date) 
                VALUES (nextval('item_id_seq'),'"""+str(item_type)+"""','"""+str(item_price)+"""', current_date, current_date);"""
    cur.execute(sql_txt)
    conn.commit()
    cur.close()
    conn.close()
