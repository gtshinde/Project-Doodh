import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user='postgres',
            password='postgres')
        return conn
    except psycopg2.Error as e:
        print("Error in connecting to PostgreSQL database")
        print("Eror Code: "+str(e.pgcode))
        print(e.pgerror)
        raise e

    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="postgres",
    #     user='postgres',
    #     password='postgres')

    # need to check how to securely pass database credentials above
    
    # return conn

def insert_users(user_email, user_name, social_media_platform):
    conn = connect()
    cur = conn.cursor()
    sql_txt = "SELECT COUNT(*) FROM users WHERE social_media_email = '"+str(user_email)+"' AND Social_Media_Type = '"+str(social_media_platform)+"';"
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

def is_admin(user_email):
    conn = connect()
    cur = conn.cursor()
    sql_txt = "SELECT Is_Admin FROM users WHERE social_media_email = '"+str(user_email)+"';" 
    cur.execute(sql_txt)  
    v_is_admin = cur.fetchone()[0]
    print(v_is_admin) 
    conn.commit()
    cur.close()
    conn.close() 
    return v_is_admin

def insert_into_items(item_type, item_price):
    try:
        conn = connect()
        with conn:
            with conn.cursor() as cur:
                sql_txt="""INSERT INTO ITEMS (Item_ID,Item_Type,Price, created_date, last_updated_date) 
                    VALUES (nextval('item_id_seq'),'"""+str(item_type)+"""','"""+str(item_price)+"""', current_date, current_date);"""
                cur.execute(sql_txt)
    except psycopg2.OperationalError as e:
        print("Operational Error occured, Eror Code: "+str(e.pgcode))
        print(e.pgerror)
    except psycopg2.Error as e:
        print("Error occured, Eror Code: "+str(e.pgcode))
        print(e.pgerror)
        raise e
    finally:
        conn.close()

def insert_into_change(item_id, item_qty):
    conn = connect()
    cur = conn.cursor()
    get_records="""SELECT COUNT(1) FROM Change_Details WHERE ITEM_ID="""+str(item_id)+"""AND Change_DATE=current_date;"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('count is ', count)
    
    if  count > 0 :
        sql_txt_update="""UPDATE Change_Details SET QTY = """+str(item_qty)+""" 
                            WHERE ITEM_ID="""+str(item_id)+""" AND Change_DATE=current_date;"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_insert="""INSERT INTO Change_Details (Change_ID,Item_ID,Change_DATE,qty) 
                VALUES (nextval('Change_ID'),'"""+str(item_id)+"""',current_date,'"""+str(item_qty)+"""');"""
        cur.execute(sql_txt_insert)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_default(item_id, item_qty, user_email_id, eff_date_from):
    conn = connect()
    cur = conn.cursor()
    get_records = """SELECT COUNT(1) FROM default_details 
                        WHERE item_id= '"""+str(item_id)+"""'
                        AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(user_email_id)+"""')
                        AND Effective_From = TO_DATE('"""+str(eff_date_from)+"""','YYYY-MM-DD');"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('Count is ', count)
    if (count > 0):
        sql_txt_update = """UPDATE default_details SET qty = '"""+str(item_qty)+"""', last_updated_date = current_date
                                WHERE item_id = '"""+str(item_id)+"""' 
                                    AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(user_email_id)+"""')
                                    AND Effective_From = TO_DATE('"""+str(eff_date_from)+"""','YYYY-MM-DD');"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_prev_update = """UPDATE default_details SET effective_to = TO_DATE('+"""+str(eff_date_from)+"""', 'YYYY-MM-DD') - 1
                                    WHERE item_id = '"""+str(item_id)+"""'
                                        AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(user_email_id)+"""')
                                        AND effective_to IS NULL;"""
        cur.execute(sql_txt_prev_update)
        sql_txt_insert="""INSERT INTO default_details (default_id, item_id, qty, user_id, created_date, last_updated_date,Effective_From) 
                            VALUES (nextval('default_id'),'"""+str(item_id)+"""','"""+str(item_qty)+"""', (SELECT user_id FROM users WHERE social_media_email = '"""+str(user_email_id)+"""'), current_date, current_date,TO_DATE('"""+str(eff_date_from)+"""','YYYY-MM-DD'));"""
        cur.execute(sql_txt_insert)
    conn.commit()
    cur.close()
    conn.close()
