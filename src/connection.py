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
def verify_user_exists(user_id):
    conn=connect()
    cur=conn.cursor()
    sql_txt = "SELECT COUNT(*) FROM users WHERE user_id = '"+str(user_id)+"';" 
    cur.execute(sql_txt)
    count = cur.fetchone()[0]
    print('count of user exists is ', count)
    return count
def verify_useremail_exists(user_email):
    conn=connect()
    cur=conn.cursor()
    sql_txt = "SELECT COUNT(*) FROM users WHERE social_media_email = '"+str(user_email)+"';" 
    cur.execute(sql_txt)
    count = cur.fetchone()[0]
    print('count of useremail exists is ', count)
    return count

def get_user_email(user_id):

    print('conn user_id:',user_id)
    count=verify_user_exists(user_id)
    if count!=0:
        conn = connect()
        cur = conn.cursor()
        sql_txt = "SELECT social_media_email FROM users WHERE user_id = '"+str(user_id)+"';" 
        cur.execute(sql_txt)
        useremail = cur.fetchone()[0]
        print('user is ', useremail)
        conn.commit()
        cur.close()
        conn.close()
        return useremail
    return 0

def get_user_id(user_email):
 
    print('conn user_id:',user_email)
    count=verify_useremail_exists(user_email)
    if count!=0:
        conn = connect()
        cur = conn.cursor()
        sql_txt = "SELECT user_id FROM users WHERE social_media_email = '"+str(user_email)+"';" 
        cur.execute(sql_txt)
        userid = cur.fetchone()[0]
        print('user is ', userid)
        conn.commit()
        cur.close()
        conn.close()
        return userid
    return 0

def validate_user_signin(user_id):

    print('conn user_id:',user_id)
    count=verify_user_exists(user_id)
    if count!=0:
        conn = connect()
        cur = conn.cursor()
        sqltext="SELECT signed_in FROM USERS WHERE user_id='"+str(user_id)+"';"
        cur.execute(sqltext)
        user_signed = cur.fetchone()[0]
        sqltext="SELECT is_admin FROM USERS WHERE user_id='"+str(user_id)+"';"
        cur.execute(sqltext)
        is_admin = cur.fetchone()[0]  
        sqltext="SELECT Social_Media_Email FROM USERS WHERE user_id='"+str(user_id)+"';"
        cur.execute(sqltext)
        user_email = cur.fetchone()[0]    
        sqltext="SELECT Social_Media_Name FROM USERS WHERE user_id='"+str(user_id)+"';"
        cur.execute(sqltext)
        user_name = cur.fetchone()[0]      
        user_details = [user_signed,is_admin,user_email,user_name]
        print('user sigined in check: ', user_signed)
        print('user admin  check: ', is_admin)
        print('user name  check: ', user_email) 
        print('user user_name  check: ', user_name)   
        print('user_detaisl:',user_details)
        conn.commit()
        cur.close()
        conn.close()
       
    else:
        user_details = [False,False,'','']
    return user_details        

def update_user_signin_status(user_email,sigin_val):
    conn = connect()
    cur = conn.cursor()
    print('conn user_email:',user_email)
    sqltext="UPDATE USERS SET signed_in='"+str(sigin_val)+"'WHERE social_media_email = '"+str(user_email)+"';" 
    cur.execute(sqltext)
    conn.commit()
    cur.close()
    conn.close()
       

def insert_users(user_email, user_name, social_media_platform,user_pwd):
    conn = connect()
    cur = conn.cursor()
    first_sigin=False                     
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
        first_sigin=True                        
    else:
        print('This email already exists!')
    
    conn.commit()
    cur.close()
    conn.close()
    return count,first_sigin

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

def insert_into_change(item_id, item_qty, email_id,past_date):
    conn = connect()
    cur = conn.cursor()
    print('printing past_date in connection:',past_date)
    if (past_date=="current_date+1"):
        past_date='current_date+1'
    else:
        past_date="""to_date('"""+str(past_date)+"""','YYYY-MM-DD')"""

    get_records="""SELECT COUNT(1) 
                    FROM Change_Details 
                    WHERE ITEM_ID="""+str(item_id)+"""
                    AND Change_DATE="""+str(past_date)+"""
                    AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""');"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('count is ', count)
    
    if  count > 0 :
        sql_txt_update="""UPDATE Change_Details SET QTY = """+str(item_qty)+""" 
                            WHERE ITEM_ID="""+str(item_id)+""" 
                            AND Change_DATE="""+str(past_date)+"""
                            AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""');"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_insert="""INSERT INTO Change_Details (Change_ID,Item_ID,Change_DATE,qty, user_id) 
                            VALUES (nextval('Change_ID'),'"""+str(item_id)+"""',"""+str(past_date)+""",'"""+str(item_qty)+"""', (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""'));"""
        cur.execute(sql_txt_insert)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_default(item_id, item_qty, user_id, eff_date_from):
    conn = connect()
    cur = conn.cursor()
    get_records = """SELECT COUNT(1) FROM default_details 
                        WHERE item_id= '"""+str(item_id)+"""'
                        AND user_id = '"""+str(user_id)+"""'
                        AND Effective_From = TO_DATE('"""+str(eff_date_from)+"""','YYYY-MM-DD');"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('Count is ', count)
    if (count > 0):
        sql_txt_update = """UPDATE default_details SET qty = '"""+str(item_qty)+"""', last_updated_date = current_date
                                WHERE item_id = '"""+str(item_id)+"""' 
                                    AND user_id = '"""+str(user_id)+"""'
                                    AND Effective_From = TO_DATE('"""+str(eff_date_from)+"""','YYYY-MM-DD');"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_prev_update = """UPDATE default_details SET effective_to = TO_DATE('+"""+str(eff_date_from)+"""', 'YYYY-MM-DD') - 1
                                    WHERE item_id = '"""+str(item_id)+"""'
                                        AND user_id = '"""+str(user_id)+"""'
                                        AND effective_to IS NULL;"""
        cur.execute(sql_txt_prev_update)
        sql_txt_insert="""INSERT INTO default_details (default_id, item_id, qty, user_id, created_date, last_updated_date,Effective_From) 
                            VALUES (nextval('default_id'),'"""+str(item_id)+"""','"""+str(item_qty)+"""', '"""+str(user_id)+"""', current_date, current_date,TO_DATE('"""+str(eff_date_from)+"""','YYYY-MM-DD'));"""
        cur.execute(sql_txt_insert)
    conn.commit()
    cur.close()
    conn.close()

def get_user_pwd_from_db(user_email):
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
    print("report_logic("+str(month)+", "+str(year)+", "+str(user_email)+")") #for debugging 
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
    num_days_in_month = num_days_in_month[1] #The abv line returns a tuple e.g(4,30) which means APR month 30 days, we want 30 days so FromDate[1]
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
                            # for the report_list[day-1] - for this day if there is value None, it means we have to add the value from the database 
                            # first iteration it will be None, so if we get Cow Milk, it will get added here
                            # next iteration, if buffalo milk is there for the same day, if None condition will not be satisfied
                            #  therefore for buffalo milk it will go to the else condition wherein we will append insteaad of '='
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

    # if(report_list = [None]*calendar.monthrange(int(year), int(month))[1]):
    #     pass
    return report_list

def check_default_details(user_id): #function to check if user has entered any default details when they login 1st time, if not then  re-direct them to the default pg again
    conn = connect()
    with conn:
        with conn.cursor() as cur:
            sql_txt="""SELECT count(default_id) FROM DEFAULT_DETAILS WHERE USER_ID='"""+str(user_id)+"""';"""
            try:
                cur.execute(sql_txt)
                count=cur.fetchone()[0]
            except Exception as e:
                print(e)
                raise e
    return count