# from operator import methodcaller
# from crypt import methods
from passlib.hash import sha256_crypt
from operator import is_
from re import sub
from flask import Flask, render_template, redirect, request, url_for
import connection
from datetime import date
import calendar
from pandas import DateOffset


is_admin = False

first_usersigin = [None]*53687091  #global variable issue won't come for this var coz the array will be updated based
                                   # on user_id as the position so each user will have their own values,max postns that array can hold are 536870912 but it's giving memory error for this val

app = Flask(__name__, template_folder='../templates', static_folder="../static")

@app.route("/")
def redirect_to_create():
    return redirect(url_for("signin"))
    # this will redirect to the signin() python url_not_foundction

@app.route("/signout/<user_email>")
def signout(user_email):
      connection.update_user_signin_status(user_email,'N')                                         
      return redirect(url_for("signin"))

@app.route("/create/<user_id>-<display_date>",methods = ["GET", "POST"])
def create(user_id, display_date):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]
    email_id=connection.get_user_email(user_id)
    print('display_date', display_date)
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):
        if (request.method == "POST"):
            # past_date = request.form.get("")
            # if(past_date is NULL):
                # past_date = "current_date+1"
            item_id = 1
            item_qty = request.form.get("cm")
            if (item_qty != '0.0'):
                connection.insert_into_change(item_id, item_qty,email_id)  
            item_id = 2
            item_qty = request.form.get("bm")
            if (item_qty != '0.0'):
                connection.insert_into_change(item_id, item_qty,email_id)  
            submitted = "Yes"
            return render_template("create.html", submitted=submitted, is_admin=is_admin,user_email=user_email,user_id=user_id, display_date=display_date)
        submitted = "No"
        return render_template("create.html",submitted=submitted,is_admin=admin,user_email=user_email,user_id=user_id, display_date=display_date)
    else:
        return render_template("url_not_found.html") 

@app.route("/report/<user_id>/<FromDate>")
def report(user_id,FromDate):
    print('FRomDate is:',FromDate)
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin): 
        # if user has not provided the month or year
        # find the system month and year
        todays_date = date.today()
        month = int(todays_date.month)
        year = int(todays_date.year)
        month_string = calendar.month_name[month]
        report_list = connection.report_logic(month, year, user_email )
        past_months_list = []
        for i in range(1, 6):
            offset_date = todays_date - DateOffset(months=i)
            past_months_list.append([str(offset_date.month), str(offset_date.year), calendar.month_name[offset_date.month]])
        # past_month_list = [ [3, 2022, March], [2, 2022, February], [1, 2022, January], ... ] considering current_date is in APRIL 2022
        print (report_list)
        print (len(report_list))
        # if FromDate=='null':
        #     FromDate= calendar.monthrange(int(year), int(month)) #get no. of days in that month, will be used to display data for all days in that month when page loads
        #     FromDate=str(FromDate[1])  #The abv line returns a tuple e.g(4,30) which means APR month 30 days, we want 30 days so FromDate[1]
        #     print('On pg load FRomDate:',FromDate)
        if FromDate!='null':
            FromDate=str(int(FromDate))+' '+month_string+' '+str(year)
        print('FRomDate after modifcation is:',FromDate)
        return render_template("report.html",is_admin=admin, report_list=report_list, month_string=month_string, past_months_list=past_months_list,user_email=user_email,user_id=user_id,FromDate=FromDate)
    else:
        return render_template('url_not_found.html')
        
@app.route("/report/<user_id>/<month>/<year>")
def report_month_year(user_id,month, year):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)  
    if (signin):    
        report_list = connection.report_logic(month, year, user_email )
        month_string = calendar.month_name[int(month)]
        past_months_list = []
        todays_date = date.today()
        for i in range(1, 6):
            offset_date = todays_date - DateOffset(months=i)
            past_months_list.append([str(offset_date.month), str(offset_date.year), calendar.month_name[offset_date.month]])
        # past_month_list = [ [3, 2022, March], [2, 2022, February], [1, 2022, January], ... ] considering current_date is in APRIL 2022
        print (report_list)
        print (len(report_list))        
        return render_template("report.html",is_admin=admin, report_list=report_list, month_string=month_string, past_months_list=past_months_list,user_email=user_email,user_id=user_id) 
    else:
        return render_template('url_not_found.html') 

@app.route("/default/<user_id>", methods=["GET", "POST"])
def default(user_id):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)
    
    if (signin):
        if(request.method == "POST"):
            
            postInfo = request.get_json()
            print(postInfo)
            userEmailID = postInfo['emailID']
            effDateFrom = postInfo['effDateFrom']
            item_id = 1
            # item_qty = request.form.get("cm")
            item_qty = postInfo['cmQty']
            if(item_qty != '0.0'):
                connection.insert_into_default(item_id, item_qty, userEmailID,effDateFrom)
                print('connection.insert_into_default(1, '+str(item_qty)+', '+str(postInfo)+', '+str(effDateFrom))
            item_id = 2
            # item_qty = request.form.get("bm")
            item_qty = postInfo['bmQty']
            if (item_qty != '0.0'):
                connection.insert_into_default(item_id, item_qty, userEmailID,effDateFrom)
                print('connection.insert_into_default(2, '+str(item_qty)+', '+str(postInfo)+', '+str(effDateFrom))
            print("submitted val in default post:",submitted)
            submitted="Yes"
            return render_template("default.html",submitted=submitted,is_admin=admin,user_email=user_email,user_id=user_id)
        submitted="No"
        return render_template("default.html",is_admin=admin,user_email=user_email,user_id=user_id,submitted=submitted)
    else:
        return render_template('url_not_found.html')

@app.route("/items/<user_id>", methods = ["GET", "POST"])
def items(user_id):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):
        if(request.method == "POST"):
            item_name = request.form.get("ItemName")
            item_price = request.form.get("ItemPrice")
            try:
                connection.insert_into_items(item_name, item_price)
            except Exception as e:
                submitted = "No"
                display_error_message = """We were unable to enter the item to the database. 
                                        Error details:
                                        """+str(e)
                return render_template("admin.html", submitted=submitted, display_error_message=display_error_message,user_email=user_email,user_id=user_id)
            submitted = "Yes"
            return render_template("admin.html", submitted=submitted, is_admin=admin,user_email=user_email,user_id=user_id)

        if ( admin ):
            submitted = "No"
            return render_template("admin.html", submitted=submitted, is_admin=admin,user_email=user_email,user_id=user_id)
        else:
            return redirect(url_for("create", user_id=user_id, display_date=False))
    else:
        return render_template("url_not_found.html")

@app.route("/signin",methods = ["GET" , "POST"])
def signin():
    global first_usersigin
                    
    display_error_message=""
    if(request.method == "GET"):
        referrer = request.referrer
        print(type(referrer))
        print('req  is coming from:',referrer)
        # if referrer=="http://localhost:5000/signup": 
        #     # connection.call_first_signin(first_sigin[1])
        #     first_usersigin[user_id]=True
        #     print('came to false')
        # print('req is coming from:',referrer)
    if(request.method == "POST"):
        user_email  = request.form.get("email")
        user_pwd  = request.form.get("password")
        user_id=connection.get_user_id(user_email)
        print('signin',user_email)
        print('signin',user_pwd)    
        print('user_id',user_id)
        db_pwd= connection.validate_user(user_email)
        print('db_pwd',db_pwd) 
        if db_pwd=='':
            db_pwd='invalidgooglepwd'  #to handle invalid google login in the login pg
        if (db_pwd==0):
            print('User with this email id has not signed up, please signup')
            display_error_message="User with this email id has not signed up,''\n'' please signup!"
        elif(sha256_crypt.verify(user_pwd, db_pwd)):
            connection.update_user_signin_status(user_email,'Y')
            print(first_usersigin[user_id])
            if(first_usersigin[user_id]):
                first_usersigin[user_id]=False
                return redirect(url_for("default",user_id=user_id))
            else:
                return redirect(url_for("create",user_id=user_id, display_date=False))
            
        else:
            print('Invalid credentials!')
            display_error_message="Invalid credentials!"
    return render_template("signin.html",display_error_message=display_error_message)

@app.route("/signin-success/<social_media_platform>/<user_email>/<user_name>")
def signin_success(social_media_platform, user_email, user_name):
    global first_usersigin
    connection.update_user_signin_status(user_email,'Y')
    user_id=connection.get_user_id(user_email)
    user_details=connection.validate_user_signin(user_id) #if a google user signins first time, record for this user wont be inserted into db at this pt in the code, goto connection.py for more clarity on this
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    referrer=request.referrer
    print('req  is coming from:',referrer)
    #signin status should be true ONLY when on success route comes from signin page, nobody shd manually enter this url and let the insertion of the users happen in the db
    if referrer=="http://localhost:5000/signin":
        signin=True
        admin=False
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):
        print(social_media_platform)
        print(user_email)
        print(user_name)
        print('google user',user_email) 
        print('google user_id',user_id)
        count,first_sigin=connection.insert_users(user_email, user_name, social_media_platform,'')
        connection.update_user_signin_status(user_email,'Y')
        user_id=connection.get_user_id(user_email)
        print("count after insert is:",count)
        if count==0:  #first signin shd be set to True only when NEW google user signs in, withotu this condition it would always set firstsign in to True when google user logs in
            first_usersigin[user_id]=True
        if(first_usersigin[user_id]):
            first_usersigin[user_id]=False
            return redirect(url_for("default",user_id=user_id))
        else:
            return redirect(url_for("create",user_id=user_id, display_date=False))
    else:
        return render_template("url_not_found.html")
@app.route("/signup",methods = ["GET", "POST"])
def signup():
    global first_usersigin
    if ( request.method== "POST"):
        user_email = request.form.get("email")
        user_name  = request.form.get("username")
        user_pwd  = request.form.get("password")
        social_media_platform = ''
        print(user_email)
        print(user_name)
        print(user_pwd)
        user_pwd = sha256_crypt.encrypt(user_pwd)
        print('after hasing',user_pwd)
        count,first_signin= connection.insert_users(user_email, user_name, social_media_platform,user_pwd)
        print('the count after calling connection.insert users is:',count)
        user_id=connection.get_user_id(user_email)
        print('got the user id in sigup after insert user:',user_id)
        if count > 0 :
            submitted = "No"
            display_error_message = """This email id already exists in the database! 
                                       Please sign up with a different email id. 
                                        """ 
            return render_template("signup.html",submitted=submitted,display_error_message=display_error_message)           
        # return redirect(url_for("create"))
        # is_admin = connection.is_admin(user_email)
        # print(is_admin)  
        submitted="Yes" 
        first_usersigin[user_id]=True
        return render_template("signup.html",submitted=submitted)
    submitted="No"
    return render_template("signup.html",submitted=submitted)

if __name__ == "__main__":
    app.run(debug=True)