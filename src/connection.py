import psycopg2
import calendar

from server import report

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
        raise Exception("Error in connecting to PostgreSQL database")

    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="postgres",
    #     user='postgres',
    #     password='postgres')

    # need to check how to securely pass database credentials above
    
    # return conn

def insert_users(user_email, user_name, social_media_platform,user_pwd):
    conn = connect()
    cur = conn.cursor()
    print('conn email',user_email)
    print('conn name',user_name)
    print('conn',social_media_platform)
    print('conn',user_pwd)
    sql_txt = "SELECT COUNT(*) FROM users WHERE social_media_email = '"+str(user_email)+"';" 
    cur.execute(sql_txt)
    count = cur.fetchone()[0]
    print('count is ', count)
    if  count == 0 :
        sql_txt_insert="""INSERT INTO users
                        VALUES (nextval('User_ID'), '"""+str(user_name)+"""', '"""+str(user_email)+"""', '"""+str(social_media_platform)+"""', 'N','"""+str(user_pwd)+"""');"""
        cur.execute(sql_txt_insert)
    else:
        print('This email already exists!')
    
    conn.commit()
    cur.close()
    conn.close()
    return count

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
        raise Exception("An operational error occured in the database. Please try again")
    except psycopg2.DataError as e:
        print("Error occured, Eror Code: "+str(e.pgcode))
        print(e.pgerror)
        raise Exception("A data error occured. Please recheck your inputs and try again.")
    except psycopg2.Error as e:
        print("Error occured, Eror Code: "+str(e.pgcode))
        print(e.pgerror)
        raise Exception("An error occured in the database. Please recheck your inputs and try again.")
    finally:
        conn.close()

def insert_into_change(item_id, item_qty, email_id):
    conn = connect()
    cur = conn.cursor()
    get_records="""SELECT COUNT(1) 
                    FROM Change_Details 
                    WHERE ITEM_ID="""+str(item_id)+"""
                    AND Change_DATE=current_date+1
                    AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""');"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('count is ', count)
    
    if  count > 0 :
        sql_txt_update="""UPDATE Change_Details SET QTY = """+str(item_qty)+""" 
                            WHERE ITEM_ID="""+str(item_id)+""" 
                            AND Change_DATE=current_date+1
                            AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""');"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_insert="""INSERT INTO Change_Details (Change_ID,Item_ID,Change_DATE,qty, user_id) 
                            VALUES (nextval('Change_ID'),'"""+str(item_id)+"""',current_date+1,'"""+str(item_qty)+"""', (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""'));"""
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

def validate_user(user_email):
    conn = connect()
    cur = conn.cursor()   
    get_count = """SELECT count(password) FROM users 
                        WHERE Social_Media_email= '"""+str(user_email)+"""';"""    
    get_pwd = """SELECT password FROM users 
                        WHERE Social_Media_email= '"""+str(user_email)+"""';"""
    cur.execute(get_count)
    pwd_count = cur.fetchone()[0]
    print('conn pwd_count is ', pwd_count)  
    if pwd_count==1:                      
        cur.execute(get_pwd)
        pwd = cur.fetchone()[0]
        print('conn pwd is ', pwd)  
    else:
        pwd=0
    conn.commit()
    cur.close()
    conn.close()    
    return pwd; 

def report_logic(month, year, user_email):
    # first need to get the default milk data for the entire month
    report_list = default_report_logic(month, year, user_email)
    # next need to check where all there was a change
    report_list = change_report_logic(month, year, user_email, report_list)
    # next need to get the total bill for the month
    #  = bill_report_logic(report_list)
    return (report_list)

def default_report_logic(month, year, user_email):
    report_list = [None]
    # list should have same number of items as number of days of the month
    num_days_in_month = calendar.monthrange(int(year), int(month))
    num_days_in_month = num_days_in_month[1]
    report_list = report_list * (num_days_in_month)
    for day in range(1, num_days_in_month+1):
        try:
            conn = connect()
            with conn:
                with conn.cursor() as cur:
                    sql_txt="""SELECT 
                                    (SELECT i.item_type FROM items i WHERE i.item_id = dd.item_id),  
                                    dd.qty, 
                                    (SELECT i.price 
                                        FROM items i 
                                        WHERE TO_DATE('"""+str(day)+"""-"""+str(month)+"""-"""+str(year)+"""','DD-MM-YYYY') 
                                            BETWEEN i.Effective_From AND COALESCE(i.Effective_To, TO_DATE('5874897-01-01','YYYY-MM-DD'))
                                            AND i.item_id = dd.item_id)
                                FROM default_details dd
                                WHERE TO_DATE('"""+str(day)+"""-"""+str(month)+"""-"""+str(year)+"""','DD-MM-YYYY') between dd.Effective_From AND COALESCE(dd.Effective_To, TO_DATE('5874897-01-01','YYYY-MM-DD')) 
                                    AND dd.user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(user_email)+"""');"""
                    cur.execute(sql_txt)
                    for record in cur.fetchall():
                        print("Date = "+str(day)+" "+calendar.month_name[int(month)]+" "+str(year))
                        print("Type = "+str(record[0]))
                        print("Qty = "+str(record[1]))
                        print("Price = "+str(record[2]))
                        if(report_list[day-1] is None):
                            report_list[day-1] = [{"date": str(day)+" "+calendar.month_name[int(month)]+" "+str(year), "type": record[0], "qty": record[1], "price": record[2]}]
                        else:
                            report_list[day-1].append({"date": str(day)+" "+calendar.month_name[int(month)]+" "+str(year), "type": record[0], "qty": record[1], "price": record[2]})
        except Exception as e:
            print(e)
            raise e
        finally:
            conn.close()
    return report_list

def change_report_logic(month, year, user_email, report_list):
    conn = connect()
    with conn:
        with conn.cursor() as cur:
            sql_txt = """SELECT (SELECT i.item_type FROM items i WHERE i.item_id = cd.item_id) item_type, cd.qty, cd.change_date, DATE_PART('day',cd.change_date)
                            FROM change_details cd
                            WHERE cd.user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(user_email)+"""')
                            AND DATE_PART('month', cd.change_date) =  '"""+str(month)+"""';"""
            cur.execute(sql_txt)
            for record in cur.fetchall():
                item_type = record[0]
                item_qty = record[1]
                # change_date = record[2]
                change_day = record[3]
                for i in range (0, len(report_list[int(change_day)-1])):
                    if (report_list[int(change_day)-1][i]['type'] == item_type):
                        report_list[int(change_day)-1][i]['qty'] = item_qty
                else:
                    pass
    return report_list