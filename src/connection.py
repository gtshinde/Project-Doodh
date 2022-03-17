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

def insert_users(user_email, user_name, social_media_platform):
    conn = connect()
    cur = conn.cursor()
    sql_txt = "SELECT COUNT(*) FROM users WHERE Social_Media_Username = '"+str(user_email)+"' AND Social_Media_Type = '"+str(social_media_platform)+"';"
    cur.execute(sql_txt)
    count = cur.fetchone()[0]
    print('count is ', count)
    if  count == 0 :
        sql_txt_insert="""INSERT INTO users
                        VALUES (nextval('User_ID'), '"""+str(user_name)+"""', '"""+str(user_email)+"""', '"""+str(social_media_platform)+"""', 'N');"""
        cur.execute(sql_txt_insert)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_items(item_type, item_price):
    conn = connect()
    cur = conn.cursor()
    sql_txt="""INSERT INTO ITEMS (Item_ID,Item_Type,Price, created_date, last_updated_date) 
                VALUES (nextval('item_id_seq'),'"""+str(item_type)+"""','"""+str(item_price)+"""', current_date, current_date);"""
    cur.execute(sql_txt)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_change(item_id, item_qty):
    conn = connect()
    cur = conn.cursor()
    get_records="""SELECT COUNT(1) FROM Change_Details WHERE ITEM_ID="""+str(item_id)+"""AND Change_DATE=current_date;"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('count is ', count)
    
    if  count > 0 :
        sql_txt_update="""UPDATE Change_Details SET QTY="""+str(item_qty)+""" WHERE ITEM_ID="""+str(item_id)+"""AND Change_DATE=current_date;"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_insert="""INSERT INTO Change_Details (Change_ID,Item_ID,Change_DATE,qty) 
                VALUES (nextval('Change_ID'),'"""+str(item_id)+"""',current_date,'"""+str(item_qty)+"""');"""
        cur.execute(sql_txt_insert)
    conn.commit()
    cur.close()
    conn.close()
