from logging import exception
from tkinter import E
import psycopg2
import calendar
from pandas import to_datetime
import datetime
from datetime import date
import calendar
from pandas import DateOffset, to_datetime
from pprint import pprint

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

def verify_milkman_exists(milkman_id):
    conn=connect()
    cur=conn.cursor()
    sql_txt = "SELECT COUNT(*) FROM milkman WHERE milkman_id = '"+str(milkman_id)+"';" 
    cur.execute(sql_txt)
    count = cur.fetchone()[0]
    print('count of milkman_id exists is ', count)
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

def get_user_name(user_email):
    print('conn user_id:',user_email)
    count=verify_useremail_exists(user_email)
    if count!=0:
        conn = connect()
        cur = conn.cursor()
        sql_txt = "SELECT Social_Media_name FROM users WHERE social_media_email = '"+str(user_email)+"';" 
        cur.execute(sql_txt)
        user = cur.fetchone()[0]
        print('user is ', user)
        conn.commit()
        cur.close()
        conn.close()
        return user
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

def update_user_signin_status(user_milkman,user_milkman_val,sigin_val):
    conn = connect()
    cur = conn.cursor()
    print('conn user_email:',user_milkman_val)
    sqltext="UPDATE USERS SET signed_in='"+str(sigin_val)+"'WHERE user_id = '"+str(user_milkman_val)+"';" 
    sqlmilkman="UPDATE milkman SET signed_in='"+str(sigin_val)+"'WHERE milkman_id = '"+str(user_milkman_val)+"';" 
    if user_milkman=='User':
        print('inside user sign in update')
        cur.execute(sqltext)
    elif user_milkman=='Milkman':
        print('inside milkman sign in update')
        cur.execute(sqlmilkman)
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
        sql_txt_insert="""INSERT INTO users (user_id,social_media_name,social_media_email,social_media_type,is_admin,password)
                        VALUES (nextval('User_ID'), '"""+str(user_name)+"""', '"""+str(user_email)+"""', '"""+str(social_media_platform)+"""', False,'"""+str(user_pwd)+"""');"""
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

def insert_into_items(item_type, item_price, effective_date_from):
    try:
        conn = connect()
        with conn:
            with conn.cursor() as cur:
                check_item_exists = """SELECT count(*)
                                FROM ITEMS
                                WHERE  item_type='"""+str(item_type)+"""'"""
               #Distinct because there could be more than 1 entries for same item
                item_type_txt = """SELECT DISTINCT item_type_id
                                FROM ITEMS
                                WHERE  item_type='"""+str(item_type)+"""'"""                                
                cur.execute(check_item_exists)
                item_exists_count = str(cur.fetchone()[0])
                print('Val of item_exists_count:',item_exists_count)
                if int(item_exists_count)==0:  #item doesn't exists so increment item_type_seq and add new item type
                    item_type_id="nextval('item_type_id_seq')"
                    insert_or_update=0
                else:                           #else take the exisitng item_type_seq and use the same either  for insertion or updation
                    cur.execute(item_type_txt)
                    item_type_id = str(cur.fetchone()[0])
                    #Insert when fresh record is there and update when for same item and same date price needs to be updated
                    insert_or_update = """SELECT count(*)
                                FROM ITEMS
                                WHERE  item_type='"""+str(item_type)+"""'
                                AND effective_from=TO_DATE('"""+str(effective_date_from)+"""','YYYY-MM-DD')"""
                    cur.execute(insert_or_update)
                    insert_or_update=cur.fetchone()[0]
                print('Val of item_type_id:',item_type_id)
                print('Val of insert_or_update:',insert_or_update)
                if insert_or_update==0: 
                    sql_txt_prev_update = """UPDATE ITEMS SET effective_to = TO_DATE('+"""+str(effective_date_from)+"""', 'YYYY-MM-DD') - 1
                                                WHERE item_type='"""+str(item_type)+"""'   
                                                    AND effective_to IS NULL;"""
                    cur.execute(sql_txt_prev_update)                    
                    sql_txt="""INSERT INTO ITEMS (Item_ID,item_type_id,Item_Type,Price, created_date, last_updated_date,effective_from) 
                               VALUES (nextval('item_id_seq'),"""+item_type_id+""",'"""+str(item_type)+"""','"""+str(item_price)+"""', current_date, current_date,TO_DATE('"""+str(effective_date_from)+"""','YYYY-MM-DD'));"""
                else:
                    sql_txt="""UPDATE ITEMS SET Price="""+str(item_price)+"""
                                WHERE  item_type='"""+str(item_type)+"""'
                                AND effective_from=TO_DATE('"""+str(effective_date_from)+"""','YYYY-MM-DD')"""
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

def insert_into_change(item_id, item_qty, email_id,from_date,to_date):
    conn = connect()
    cur = conn.cursor()
    print('printing from_date in connection:',from_date)
    print('printing to_date in connection:',to_date)
    # if (past_date=="current_date+1"):
    #     past_date='current_date+1'
    # else:
    #     past_date="""to_date('"""+str(past_date)+"""','YYYY-MM-DD')"""

    get_records="""SELECT COUNT(1) 
                    FROM Change_Details 
                    WHERE ITEM_ID="""+str(item_id)+"""
                            AND Effective_From=TO_DATE('"""+str(from_date)+"""','YYYY-MM-DD')
                            AND Effective_To=TO_DATE('"""+str(to_date)+"""','YYYY-MM-DD')   
                    AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""');"""
    cur.execute(get_records)
    count = cur.fetchone()[0]
    print('count is ', count)
    
    if  count > 0 :
        sql_txt_update="""UPDATE Change_Details SET QTY = """+str(item_qty)+""" 
                            WHERE ITEM_ID="""+str(item_id)+""" 
                            AND Effective_From=TO_DATE('"""+str(from_date)+"""','YYYY-MM-DD')
                            AND Effective_To=TO_DATE('"""+str(to_date)+"""','YYYY-MM-DD')                          
                            AND user_id = (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""');"""
        cur.execute(sql_txt_update)
    else:
        sql_txt_insert="""INSERT INTO Change_Details (Change_ID,Item_ID,qty, user_id,Effective_From,Effective_To) 
                            VALUES (nextval('Change_ID'),'"""+str(item_id)+"""','"""+str(item_qty)+"""', (SELECT user_id FROM users WHERE social_media_email = '"""+str(email_id)+"""'),TO_DATE('"""+str(from_date)+"""','YYYY-MM-DD'),TO_DATE('"""+str(to_date)+"""','YYYY-MM-DD'));"""
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

def get_default_details(item_id, user_id, effective_date_from):
    default_qty = None
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                sql_text = """SELECT qty
                                FROM default_details
                                WHERE   item_id ='"""+str(item_id)+"""' 
                                    AND user_id = '"""+str(user_id)+"""' 
                                    AND TO_DATE('"""+str(effective_date_from)+"""', 'YYYY-MM-DD') BETWEEN effective_from AND COALESCE(effective_to, TO_DATE('5874897-01-01','YYYY-MM-DD'))"""
                cur.execute(sql_text)
                default_qty = cur.fetchone()[0]
    except Exception as e:
        print(e)
        raise(e)
    finally:
        conn.close()
        return default_qty
        # this value will be the value of the default_quantity or else if any error, it will be None

def get_user_pwd_from_db(user_milkman,user_type):  #user_milkman is milkman_id which is being passed when the calling function is related to milkman
    conn = connect()
    cur = conn.cursor()   
    get_count = """SELECT count(password) FROM users 
                        WHERE Social_Media_email= '"""+str(user_milkman)+"""';"""    
    get_pwd = """SELECT password FROM users 
                        WHERE Social_Media_email= '"""+str(user_milkman)+"""';"""
    get_milkman_count = """SELECT count(password) FROM milkman 
                        WHERE milkman_id= '"""+str(user_milkman)+"""';"""    
    get_milkman_pwd = """SELECT password FROM milkman 
                        WHERE milkman_id= '"""+str(user_milkman)+"""';"""
    if user_type=='User':
        print('User type is user: ',user_type)
        cur.execute(get_count)
    elif user_type=='Milkman':
        print('User type is milkman: ',user_type)
        cur.execute(get_milkman_count)
    pwd_count = cur.fetchone()[0]
    print('conn pwd_count is ', pwd_count)  
    if pwd_count==1:  
        if user_type=='User':                    
            cur.execute(get_pwd)
        elif user_type=='Milkman':
            cur.execute(get_milkman_pwd)
        pwd = cur.fetchone()[0]
        print('conn pwd is ', pwd)  
    else:
        pwd=0
    conn.commit()
    cur.close()
    conn.close()    
    return pwd

def report_logic(from_date, to_date, user_id):
    print("From Date ", from_date),
    print("To Date: ", to_date)
    # first need to get the default milk data for the date between from_date and to_date
    print("report_logic("+str(from_date)+", "+str(to_date)+", "+str(user_id)+")") #for debugging 
    report_list = default_report_logic(from_date, to_date, user_id)
    # next need to check where all there was a change
    report_list,total_price,tomo_type_qty = change_report_logic(from_date, to_date, user_id, report_list)
    # next need to get the total bill for the month
    #  = bill_report_logic(report_list)
    return (report_list,total_price,tomo_type_qty)

def default_report_logic(from_date, to_date, user_id):
    report_list = [None]
    # list should have same number of items as number of days of the month
    from_date = to_datetime(from_date, format='%Y-%m-%d')
    to_date = to_datetime(to_date, format='%Y-%m-%d')
    #The below +1 is added to handle the case when from date=to date, the for loop will then hv range as 0-1 and it will run atleast once. Without this condition the for loop wont even run once
    #The +1 was also added in order to display today's date, else it would only go until yesterday's date
    num_days_between_fromDate_toDate = ((to_date - from_date).days)+1
    # num_days_in_month = num_days_in_month[1] #The abv line returns a tuple e.g(4,30) which means APR month 30 days, we want 30 days so FromDate[1]
   
    # if num_days_between_fromDate_toDate==0:
    #     num_days_between_fromDate_toDate+=1
    report_list = report_list * (num_days_between_fromDate_toDate)
    for day in range(0, num_days_between_fromDate_toDate):
        try:
            conn = connect()
            with conn:
                with conn.cursor() as cur:
                    sql_txt="""SELECT 
                                    (SELECT i.item_type FROM items i WHERE i.item_id = dd.item_id),  
                                    dd.qty, 
                                    (SELECT i.price*dd.qty 
                                        FROM items i 
                                        WHERE TO_DATE('"""+str((from_date+datetime.timedelta(days=day)))+"""','YYYY-MM-DD') 
                                            BETWEEN i.Effective_From AND COALESCE(i.Effective_To, TO_DATE('5874897-01-01','YYYY-MM-DD'))
                                            AND i.item_id = dd.item_id)
                                FROM default_details dd
                                WHERE TO_DATE('"""+str((from_date+datetime.timedelta(days=day)))+"""','YYYY-MM-DD') between dd.Effective_From AND COALESCE(dd.Effective_To, TO_DATE('5874897-01-01','YYYY-MM-DD')) 
                                    AND dd.user_id = '"""+str(user_id)+"""';"""
                    cur.execute(sql_txt)
                    for record in cur.fetchall():
                        item_type = record[0]
                        item_qty = record[1]
                        price = record[2]                        
                        print("Date = "+str((from_date+datetime.timedelta(days=day))).split(" ")[0])
                        # Eg: split function will give ['2022-04-15', '00:00:00'] - so we only need [0]
                        print("Type = "+str(record[0]))
                        print("Qty = "+str(record[1]))
                        print("Price = "+str(record[2]))
                        if (item_qty==0):
                            price=0
                        if(report_list[day] is None):
                            # for the report_list[day-1] - for this day if there is value None, it means we have to add the value from the database 
                            # first iteration it will be None, so if we get Cow Milk, it will get added here
                            # next iteration, if buffalo milk is there for the same day, if None condition will not be satisfied
                            #  therefore for buffalo milk it will go to the else condition wherein we will append insteaad of '='
                            report_list[day] = [{"date": str((from_date+datetime.timedelta(days=day))).split(" ")[0], "type": item_type, "qty": item_qty, "price": price}]
                        else:
                            report_list[day].append({"date": str((from_date+datetime.timedelta(days=day))).split(" ")[0], "type": item_type, "qty": item_qty, "price": price})
        except Exception as e:
            print(e)
            raise e
        finally:
            conn.close()
    return report_list

def change_report_logic(from_date, to_date, user_id, report_list):
    conn = connect()
    todays_date = date.today()
    tomo_type_qty=[]
    from_date = to_datetime(from_date, format='%Y-%m-%d')
    to_date = to_datetime(to_date, format='%Y-%m-%d')
    num_days_between_fromDate_toDate = ((to_date - from_date).days)+1
    total_price=0
    for day in range(0, num_days_between_fromDate_toDate):
        with conn:
            with conn.cursor() as cur:
                #this select is going to get us the records where change had happened for a particular day
                sql_txt = """SELECT 
                                (SELECT i.item_type 
                                    FROM items i 
                                    WHERE i.item_id = cd.item_id) item_type, 
                                cd.qty, 
                                TO_DATE('"""+str((from_date+datetime.timedelta(days=day)))+"""','YYYY-MM-DD'),
                                (SELECT i.price * cd.qty
                                        FROM items i 
                                        WHERE TO_DATE('"""+str((from_date+datetime.timedelta(days=day)))+"""','YYYY-MM-DD') 
                                            BETWEEN i.Effective_From AND COALESCE(i.Effective_To, TO_DATE('5874897-01-01','YYYY-MM-DD'))
                                            AND i.item_id = cd.item_id)
                            FROM change_details cd
                            WHERE cd.user_id = '"""+str(user_id)+"""'
                                AND TO_DATE('"""+str((from_date+datetime.timedelta(days=day)))+"""','YYYY-MM-DD')
                                    BETWEEN cd.Effective_From AND COALESCE(cd.Effective_To, TO_DATE('5874897-01-01','YYYY-MM-DD'))"""
                cur.execute(sql_txt)
                #fetchall will get all the columns for each row
                for record in cur.fetchall():
                    item_type = record[0]
                    item_qty = record[1]
                    change_date = record[2]
                    price = record[3]
                    if item_qty==0:
                        price=0
                    # below for loop is for the items in default report list
                    change_present_in_default = False
                    for i in range (0, len(report_list[day])):

                        if (report_list[day][i]['type'] == item_type):
                            report_list[day][i]['qty'] = item_qty
                            report_list[day][i]['price'] = price
                            change_present_in_default = True
                            
                            break 
                            #once it matches and upadtes we don't need to check other items in default report list for that day
                    if(not change_present_in_default):
                        report_list[day].append({"date": change_date, "type": item_type, "qty": item_qty, "price": price})
                        
    
    for day_list in report_list:
        if (day_list is not None):
            for item_dict in day_list:
                total_price+=item_dict['price']
                print('Todays date:',todays_date)
                print('item_dict[date]:',item_dict['date'])
                
                if item_dict['date'] == str(todays_date):
                    print('Todays date matches')
                    tomo_type_qty.append(item_dict)
                else:
                    print('No matches')
            print('The total bill for the day is:',total_price)
    print('The total bill is:',total_price)
    print('tomo_type_qty is:',tomo_type_qty)
    return report_list,total_price,tomo_type_qty

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

def get_milkman_area_city(area,city):
    milkman_list=[]
    conn=connect()
    with conn:
         with conn.cursor() as cur:
             if (area is None and city is None):
                sql_txt="""select distinct city from locations;"""
             elif (city is not None and area is None):
                sql_txt="""select distinct area from locations where upper(city)='"""+str(city).upper()+"""';"""
             else:
                location_id=get_location_id(city,area)
                sql_txt="""select milkman_shop from milkman where location_id=CAST ('"""+str(location_id)+"""' AS INTEGER);"""
                         
             try:
                 
                 print('sqltxt',sql_txt)
                 cur.execute(sql_txt)
                 for record in cur.fetchall():
                    milkman_list.append(record[0])
             except Exception as e:
                 print(e)
                 raise e
    return milkman_list

def update_users_with_milkman(milkman_shop,user_id,location_id,address):
        print('COnn milkman_shop:',milkman_shop) 
        print('COnn user_id:',user_id) 
        print('COnn address is:',address) 
        conn=connect()
        with conn: 
           with conn.cursor() as cur:
                sql_txt="""UPDATE USERS SET ADDRESS=lower('"""+str(address)+"""')
                            ,MILKMAN_ID=(SELECT MILKMAN_ID 
                            FROM MILKMAN
                            WHERE MILKMAN_SHOP='"""+str(milkman_shop)+"""' AND location_id=CAST ('"""+str(location_id)+"""' AS INTEGER))
                            ,USER_RATING=NULL
                            WHERE USER_ID='"""+str(user_id)+"""';"""
                try:
                    cur.execute(sql_txt)
                except Exception as e:
                    print(e)
                    raise e

def view_user_milkman_details(user_id):
     conn=connect()
     with conn:
         with conn.cursor() as cur:
             sqltxt="""SELECT city,area,(select milkman_shop from milkman where milkman_id=
                        (select milkman_id from users where user_id='"""+str(user_id)+"""'))
              from locations where location_id=
                        (SELECT location_id from milkman where milkman_id=
                        (select milkman_id from users where user_id='"""+str(user_id)+"""'));"""
             try:
                cur.execute(sqltxt)
                milkman_details=cur.fetchall()
                print(milkman_details)
                 #incase when milkman is not available in the list
                if milkman_details==[]: 
                    city=None
                    area=None
                    milkman_store=None
                else:
                    city=milkman_details[0][0]
                    area=milkman_details[0][1]
                    milkman_store=milkman_details[0][2]
                print('Area in view_user_milkman_details:',area)
                print('City in view_user_milkman_details:',city)
                print('milkman in view_user_milkman_details:',milkman_store)
             except Exception as e:
                 print(e)
                 raise e
     return city,area,milkman_store

def milkman_rating(milkman_id,rating,user_id,location_id):
        print('COnn milkman_shop:',milkman_id_store(milkman_id,None,location_id)) 
        print('COnn rating:',rating) 
        conn=connect()
        with conn: 
           with conn.cursor() as cur:
                sql_update_user_rating="""UPDATE USERS SET USER_RATING='"""+str(rating)+"""' WHERE USER_ID='"""+str(user_id)+"""'"""
                sql_cnt="""SELECT count(1) FROM MILKMAN_RATING WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
                sql_insert="""INSERT INTO milkman_rating VALUES (NEXTVAL('rating_id'),'"""+str(milkman_id)+"""','"""+str(rating)+"""',1); """
                sql_user_rating="""SELECT coalesce(user_rating,0) FROM USERS WHERE USER_ID='"""+str(user_id)+"""' and MILKMAN_ID='"""+str(milkman_id)+"""';"""
                try:
                    cur.execute(sql_user_rating)
                    prev_user_rating=cur.fetchone()[0]
                    cur.execute(sql_update_user_rating)
                    cur.execute(sql_cnt)
                    count= cur.fetchone()[0]
                    # print('cur.execute(sql_cnt):',cur.execute(sql_cnt))
                    print('rating count for the milkman:',count)
                    # user_rating=cur.execute(sql_user_rating)
                    if count==0:
                        cur.execute(sql_insert)
                    else:
                        #check if the user_id has entered rating
                        print('user_id:',user_id)
                        print('initial user rating is:',prev_user_rating)
                        #overall_rating for that milkman was 10 (including 4)
                        #overall_rating=10-4+2
                        if prev_user_rating>0:
                            OVERALL_RATING="""OVERALL_RATING-'"""+str(prev_user_rating)+"""'+'"""+str(rating)+"""'"""
                            NO_OF_USERS="NO_OF_USERS"
                            print('OVERALL_RATING: ',OVERALL_RATING)
                            print('NO_OF_USERS: ',NO_OF_USERS)
                        else:
                            OVERALL_RATING="""OVERALL_RATING+'"""+str(rating)+"""'"""
                            NO_OF_USERS="""NO_OF_USERS+1"""
                            print('OVERALL_RATING: ',OVERALL_RATING)
                            print('NO_OF_USERS: ',NO_OF_USERS)
                        sql_update="""UPDATE MILKMAN_RATING SET OVERALL_RATING="""+str(OVERALL_RATING)+""", 
                                        NO_OF_USERS="""+str(NO_OF_USERS)+"""
                                        WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
                        cur.execute(sql_update)

                except Exception as e:
                    print(e)
                    raise e

def milkman_id_store(milkman_id,milkman_store,location_id):
    print('milkman_id_store-milkman_id',milkman_id)
    print('milkman_id_store-milkman_store',milkman_store)
    print('milkman_id_store-location_id',location_id)
    conn=connect()
    with conn:
        with conn.cursor() as cur:
            try:
                sql_milkman_count="""SELECT count(MILKMAN_ID) FROM MILKMAN WHERE  upper(milkman_shop)=upper('"""+str(milkman_store)+"""') AND location_id=CAST ('"""+str(location_id)+"""' AS INTEGER);"""
                sql_milkman_id="""SELECT MILKMAN_ID FROM MILKMAN WHERE  upper(milkman_shop)=upper('"""+str(milkman_store)+"""') AND location_id=CAST ('"""+str(location_id)+"""' AS INTEGER);"""
                sql_milkman_store="""SELECT lower(MILKMAN_SHOP) FROM MILKMAN WHERE  MILKMAN_ID='"""+str(milkman_id)+"""';"""
                # below if written coz we do not need to validate the milkman existance when location=' ' which is passed to load the  milkman dashboard
                # if location_id == ' ': 
                cur.execute(sql_milkman_count)
                milkman_count=cur.fetchone()[0]
                print('milkman_count:',milkman_count)
                if milkman_count ==0:
                    return 0
                if milkman_id is None:
                    cur.execute(sql_milkman_id)
                    milkman_id=cur.fetchone()[0]
                    print('milkman_id:',milkman_id)
                    return milkman_id
                elif (milkman_store is None):
                    cur.execute(sql_milkman_store)
                    milkman_store=cur.fetchone()[0]
                    print('Milkman store:',milkman_store)
                    return milkman_store
            except Exception as e: 
                print(e)
                raise(e)
  
def get_overall_rating(milkman_stores,location_id):
    print('milkman_store: ',milkman_stores)
    milkman_id=milkman_id_store(None,milkman_stores,location_id)
    print('conn milkman id : ',milkman_id)
    sql_count="""SELECT count(overall_rating) FROM MILKMAN_RATING WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
    sql_select="""SELECT COALESCE(OVERALL_RATING,0) FROM MILKMAN_RATING WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
    sql_users="""SELECT COALESCE(NO_OF_USERS,0) FROM MILKMAN_RATING WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
    conn=connect()
    with conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql_count)
                count=cur.fetchone()[0]
                print('Count of overall rating is:',count)
                #when no rating has been given to the milkman
                rating=0     
                if count>0:
                    cur.execute(sql_select)
                    overall_rate=cur.fetchone()[0]
                    cur.execute(sql_users)
                    no_of_users=cur.fetchone()[0]
                    rating=overall_rate/no_of_users
                    print('rating in conn is:',rating)
            except Exception as e:
                print(e)
                raise(e)
    return rating

def milkman_dashboard_logic(milkman_id):
    conn=connect()
    users_list=[None]
    i=0
    with conn:
        sql_get_user_count="""SELECT COUNT(USER_ID) FROM USERS WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
        sql_get_users="""SELECT Social_Media_Name,user_id,address FROM USERS WHERE MILKMAN_ID='"""+str(milkman_id)+"""';"""
        with conn.cursor() as cur:
            try:
                cur.execute(sql_get_user_count)
                user_count=cur.fetchone()[0]
                # user_count=user_count
                users_list=users_list*user_count
                cur.execute(sql_get_users)
                user_details=cur.fetchall()
                print('user_details:',user_details)
                for user in user_details:
                    user_name=user[0]
                    user_id=user[1]
                    address=user[2]
                    print('user_name:',user_name)
                    print('user_ids:',user_id)
                    print('address :',address)
                      # find the system month and year
                    todays_date = date.today()
                    month = int(todays_date.month)
                    year = int(todays_date.year)
                    print('calling the report logic from milkmandashboard')
                    report_list,total_price,tomo_type_qty =report_logic(str(year)+"-"+str(month)+"-01", str(todays_date), user_id)
                    if(users_list[i] is None):
                        users_list[i] = {"user": user_name,"user_id":user_id, "report": report_list, "total_price": total_price, "tomo_type_qty":tomo_type_qty,'address':address}
                        i=i+1

                    print('user is:',user)
                    print('user ID is:',user_id)
                    print('Dict users_list for user:')
                    print(users_list)
                print('Printing the final list')
                pprint(users_list)
            except Exception as e:
                print(e)
                raise(e)
    return user_count,users_list

#function to find single user details when milkman selects specific user from dropdown
def milkman_dashboard_single_user_logic(milkman_id,Social_Media_Name,address):
    conn=connect()
    users_list=[None]
    i=0
    with conn:
        sql_get_user_count="""SELECT COUNT(USER_ID) FROM USERS WHERE MILKMAN_ID='"""+str(milkman_id)+"""' AND address='"""+str(address)+"""' AND Social_Media_Name='"""+str(Social_Media_Name)+"""';"""
        #here in the select query Social_Media_Name is not reqd but still hv kept it so that the exisitng logic flow doest break..no harm in keeping it :-)
        sql_get_users="""SELECT Social_Media_Name,user_id FROM USERS WHERE MILKMAN_ID='"""+str(milkman_id)+"""'AND address='"""+str(address)+"""' AND Social_Media_Name='"""+str(Social_Media_Name)+"""';"""
        with conn.cursor() as cur:
            try:
                print('Inside milkman dashboard single user function')
                cur.execute(sql_get_user_count)
                user_count=cur.fetchone()[0]   #this count shd always be 1
                print('user_count: ',user_count)
                users_list=users_list*user_count
                cur.execute(sql_get_users)
                user_details=cur.fetchall()
                print('user_details:',user_details)
                for user in user_details:
                    user_name=user[0]
                    user_id=user[1]
                    print('user_name:',user_name)
                    print('user_ids:',user_id)
                      # find the system month and year
                    todays_date = date.today()
                    month = int(todays_date.month)
                    year = int(todays_date.year)
                    print('calling the report logic from milkmandashboard')
                    report_list,total_price,tomo_type_qty =report_logic(str(year)+"-"+str(month)+"-01", str(todays_date), user_id)
                    if(users_list[i] is None):
                        users_list[i] = {"user": user_name,"user_id":user_id, "report": report_list, "total_price": total_price, "tomo_type_qty":tomo_type_qty}
                        i=i+1

                    print('user is:',user)
                    print('user ID is:',user_id)
                    print('Dict users_list for user:')
                    print(users_list)
                print('Printing the final list')
                pprint(users_list)
            except Exception as e:
                print(e)
                raise(e)
    return user_count,users_list

def get_location_id(city,area):
    conn = connect()
    cur = conn.cursor()
    print('conn city',city)
    print('conn area',area)
    sql_loc= "SELECT location_id FROM locations WHERE city='"+str(city)+"' AND area='"+str(area)+"';"   
    cur.execute(sql_loc)
    location_id = cur.fetchone()[0]
    return location_id

def insert_milkman( milkman_store, milkman_pwd,city,area):
    conn = connect()
    cur = conn.cursor()
                    
    print('conn milkman_store',milkman_store)
    print('conn milkman_pwd',milkman_pwd)
    print('conn city',city)
    print('conn area',area)
    
    location_id=get_location_id(city,area)
    sql_txt = """SELECT COUNT(*) FROM milkman WHERE milkman_shop = '"""+str(milkman_store)+"""' AND location_id =CAST('"""+str(location_id)+"""' AS INTEGER);""" 
    cur.execute(sql_txt)
    count = cur.fetchone()[0]
    print('count is ', count)
    if  count == 0 :
        sql_txt_insert="""INSERT INTO milkman
                        VALUES (nextval('milkman_id'), lower('"""+str(milkman_store)+"""'),CURRENT_DATE,CURRENT_DATE,CAST("""+str(location_id)+""" AS INTEGER),False, '"""+str(milkman_pwd)+"""');"""
        cur.execute(sql_txt_insert)
                            
    else:
        print('This milkman already exists in this area!')
    
    conn.commit()
    cur.close()
    conn.close()
    return count
                    

def validate_milkman_signin(milkman_id):

    print('conn milkman_id:',milkman_id)
    count=verify_milkman_exists(milkman_id)
    if count!=0:
        conn=connect()
        with conn:
            with conn.cursor() as cur:
                try:
                    sqltext="SELECT signed_in FROM MILKMAN WHERE milkman_id='"+str(milkman_id)+"';"
                    cur.execute(sqltext)
                    signed_in = cur.fetchone()[0]      
                    print('milkman sigined in check: ', signed_in)
                except Exception as e:
                    print(e)
                    raise(e)
    return signed_in     

#below function gets the user's milkman and returns he has signed or not
def get_user_milkman_signin(user_id):
    print('conn get_user_milkman() user_id:',user_id)
    sql_txt="SELECT milkman_id FROM users WHERE user_id='"+str(user_id)+"';"
    
    conn=connect()
    with conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql_txt)
                milkman_id = cur.fetchone()[0]      
                print(' milkman_id : ', milkman_id)
                signed_in=validate_milkman_signin(milkman_id)
                sql_milkman_store="SELECT milkman_shop FROM milkman WHERE milkman_id='"+str(milkman_id)+"';"
                cur.execute(sql_milkman_store)
                milkman_store = cur.fetchone()[0]  
                print(' milkman_store : ', milkman_store)
                
            except Exception as e:
                print(e)
                raise(e)
    return signed_in,milkman_store     
