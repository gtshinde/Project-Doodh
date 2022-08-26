# from operator import methodcaller
# from crypt import methods
from pprint import pprint
from passlib.hash import sha256_crypt
from operator import is_
from re import sub
from flask import Flask, render_template, redirect, request, url_for
import importlib
# import connection
# module_name = 'connection'
# special_module = importlib.import_module(module_name, package='./src')
import src.connection as connection
from datetime import date
import calendar
from pandas import DateOffset, to_datetime


is_admin = False

first_usersigin = [None]*53687091  #global variable issue won't come for this var coz the array will be updated based
                                   # on user_id as the position so each user will have their own values,max postns that array can hold are 536870912 but it's giving memory error for this val

app = Flask(__name__, template_folder='templates', static_folder="static")

@app.route("/")
def redirect_to_create():
    return redirect(url_for("signin"))
    # this will redirect to the signin() python url_not_foundction

@app.route("/signout/<user_id>")
def signout(user_id):
      connection.update_user_signin_status('User',user_id,False)                                         
      return redirect(url_for("signin"))

@app.route("/create/<user_id>",methods = ["GET", "POST"])
def create(user_id):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]
    email_id=connection.get_user_email(user_id)
    user_name=connection.get_user_name(user_email)
    # print('display_date', display_date)
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):
        if (request.method == "POST"):
            form_data=request.form 
        #   if (display_date=='True'):
                 #request.form gets all the form data and returns it as a dictionary of key value pairs
                # past_date = request.form.get("past_date_input")
                # past_date=form_data['past_date_input']
                # print('past_date_input from form:',past_date)
            print("create pg form data :",form_data)
            from_date = form_data['fromDate']
            print('form_data[fromDate]',form_data['fromDate'])
            to_date = form_data['toDate']
            print('form_data[toDate]',form_data['toDate'])            
    #   --  else:
            # past_date = "current_date+1"
            item_id = 1
            item_qty = request.form.get("cm")
            cm=form_data['cm']
            if (item_qty != '0.0'):
                connection.insert_into_change(item_id, item_qty,email_id,from_date,to_date)  
            item_id = 2
            item_qty = request.form.get("bm")
            bm=form_data['bm']
            if (item_qty != '0.0'):
                connection.insert_into_change(item_id, item_qty,email_id,from_date,to_date) 
            submitted = "Yes"
            return render_template("create.html", submitted=submitted, is_admin=admin,user_email=user_email,user_id=user_id,cm=cm,bm=bm,form_data=form_data,user=user_name)
        submitted = "No"
        return render_template("create.html",submitted=submitted,is_admin=admin,user_email=user_email,user_id=user_id,user=user_name)
    else:
        return render_template("url_not_found.html") 

@app.route("/report/<user_id>")
def report(user_id):
    # print('FRomDate is:',FromDate)
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('Report page: user sign in status',signin)
    print('Report page:user admin status',admin)
    user_name=connection.get_user_name(user_email)
    print('Report page: Name of user: ',user_name)
    if (signin): 
        # if user has not provided the month or year
        # find the system month and year
        todays_date = date.today()
        month = int(todays_date.month)
        year = int(todays_date.year)
        month_string = calendar.month_name[month]
        report_list,total_price,tomo_type_qty = connection.report_logic(str(year)+"-"+str(month)+"-01", str(todays_date), user_id)
        past_months_list = []
        for i in range(1, 6):
            offset_date = todays_date - DateOffset(months=i)
            past_months_list.append([str(offset_date.month), str(offset_date.year), calendar.month_name[offset_date.month]])
        # past_month_list = [ [3, 2022, March], [2, 2022, February], [1, 2022, January], ... ] considering current_date is in APRIL 2022
        pprint(report_list)
        print (len(report_list))
        print('REPORT TOTAL: ',total_price)
 
        # in the below line user_type will be U always for this path coz this URL is only for user/consumer
        return render_template("report.html",is_admin=admin, report_list=report_list, month_string=month_string, past_months_list=past_months_list,user_email=user_email,user_id=user_id,total_price=total_price,user=user_name,user_type='U')  
    else:
        return render_template('url_not_found.html')
        
@app.route("/report/<user_type>-<user_id>/<month>/<year>")
# user_type means who is accessing the url, is it user/consumer(U) or the milkman(M)
def report_month_year(user_type,user_id,month, year):
    print('Person accessing this URL is: ',user_type)
    todays_date = date.today()
    todays_month = int(todays_date.month)
    todays_year = int(todays_date.year)
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)  
    user_name=connection.get_user_name(user_email)
    print('user name is:',user_name)
    if user_type == 'M':
        signin,milkman_store=connection.get_user_milkman_signin(user_id)
        user_email=milkman_store
   
    if (signin):
        num_days_in_month = calendar.monthrange(int(year), int(month))[1]   
        if (int(month)==todays_month and int(year)==todays_year): # if it is current month, report_list should diplay only till current date and not till end of month
            report_list,total_price,report_logic = connection.report_logic(str(year)+"-"+str(month)+"-01", str(todays_date) , user_id)
        else:     
            report_list,total_price,report_logic = connection.report_logic(str(year)+"-"+str(month)+"-01", str(year)+"-"+str(month)+"-"+str(num_days_in_month), user_id)
        month_string = calendar.month_name[int(month)]
        past_months_list = []
        todays_date = date.today()
        for i in range(0, 5):
            offset_date = todays_date - DateOffset(months=i)
            past_months_list.append([str(offset_date.month), str(offset_date.year), calendar.month_name[offset_date.month]])
        # past_month_list = [ [3, 2022, March], [2, 2022, February], [1, 2022, January], ... ] considering current_date is in APRIL 2022
        pprint (report_list)
        print (len(report_list))
        print('REPORT TOTAL: ',total_price)        
        return render_template("report.html",is_admin=admin, report_list=report_list, month_string=month_string, past_months_list=past_months_list,user_email=user_email,user_id=user_id,total_price=total_price,user=user_name,user_type=user_type)
    else:
        return render_template('url_not_found.html') 

# "/report/1000/2020-03-01:2020-04-21"
@app.route("/report/<user_type>-<user_id>/<from_date>:<to_date>")
def report_for_date_range(user_type,user_id, from_date, to_date):
    print('inside report_for_date_range() : Person accessing this URL is: ',user_type)
    user_details = connection.validate_user_signin(user_id)
    print('Report page (fromDate-toDate): in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('Report page (fromDate-toDate): user sign in status',signin)
    print('Report page (fromDate-toDate): user admin status',admin)  
    user=connection.get_user_name(user_email)
    print('user name is:',user)
    if user_type == 'M':
        signin,milkman_store=connection.get_user_milkman_signin(user_id)
        user_email=milkman_store
    if (signin):
        p_from_date = from_date  #storing the parameter values in string only before converting to timestamp format- this is reqd by the report.html pg (lenght function used there for from and todate won't work for timestamp values))
        p_to_date = to_date
        report_list,total_price,tomo_type_qty = connection.report_logic(from_date, to_date, user_id)
        from_date = to_datetime(from_date, format='%Y-%m-%d')
        to_date = to_datetime(to_date, format='%Y-%m-%d')
        month_string = ""
        past_months_list = []
        todays_date = date.today()
        for i in range(1, 6):
            offset_date = todays_date - DateOffset(months=i)
            past_months_list.append([str(offset_date.month), str(offset_date.year), calendar.month_name[offset_date.month]])
        # past_month_list = [ [3, 2022, March], [2, 2022, February], [1, 2022, January], ... ] considering current_date is in APRIL 2022
        pprint (report_list)
        print (len(report_list)) 
        print('REPORT TOTAL: ',total_price)
        submitted="Yes"
        return render_template("report.html",is_admin=admin, report_list=report_list, month_string=month_string, past_months_list=past_months_list,user_email=user_email,user_id=user_id,from_date=p_from_date,to_date=p_to_date,submitted=submitted,total_price=total_price,user=user,user_type=user_type) 
    else:
        return render_template('url_not_found.html')

@app.route("/default/<user_id>", methods=["GET", "POST"])
def default(user_id):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]   
    user=connection.get_user_name(user_email) 
    print('user sign in status',signin)
    print('user admin status',admin)
    print('user name is',user)
    if (signin):
        if(request.method == "POST"):
            # print("Coming inside the post block - default")
            # form_data=request.form
            # print("create pg form data :",form_data)
            # postInfo = request.get_json()
            # print(postInfo)
            # effDateFrom = postInfo['effDateFrom']
            item_id = 1
            # item_qty = request.form.get("cm")
            # item_qty = postInfo['cmQty']
            posted_info = request.form
            eff_date_from = posted_info['effectiveFrom']
            cm_item_qty = posted_info['cm']
            if(cm_item_qty != '0.0'):
                connection.insert_into_default(item_id, cm_item_qty, user_id,eff_date_from)
                print('connection.insert_into_default(1, '+str(cm_item_qty)+', '+str(posted_info)+', '+str(eff_date_from))
            else:
                # if cm_item_qty is 0.0 (no change)
                cm_item_qty = connection.get_default_details(item_id, user_id, eff_date_from)
                print('connection.get_default_details('+str(item_id)+', '+str(user_id)+', '+str(eff_date_from)+')') # for debugging
            item_id = 2
            bm_item_qty = posted_info["bm"]
            if (bm_item_qty != '0.0'):
                connection.insert_into_default(item_id, bm_item_qty, user_id,eff_date_from)
                print('connection.insert_into_default(2, '+str(bm_item_qty)+', '+str(posted_info)+', '+str(eff_date_from))
            else:
                # if bm_item_qty is 0.0 (no change)
                bm_item_qty = connection.get_default_details(item_id, user_id, eff_date_from)
                print('connection.get_default_details('+str(item_id)+', '+str(user_id)+', '+str(eff_date_from)+')') # for debugging
            submitted="Yes"
            print("Submitted", submitted)
            return render_template("default.html",submitted=submitted,is_admin=admin,user_email=user_email,user_id=user_id, eff_date_from=eff_date_from, cm_item_qty=cm_item_qty, bm_item_qty=bm_item_qty,user=user)
        submitted="No"
        print("Submitted is ", submitted)
        return render_template("default.html",is_admin=admin,user_email=user_email,user_id=user_id,submitted=submitted,user=user)
    else:
        return render_template('url_not_found.html')

@app.route("/items/<user_id>", methods = ["GET", "POST"])
def items(user_id):
    user_details=connection.validate_user_signin(user_id)
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]  
    user=connection.get_user_name(user_email)  
    print('user sign in status',signin)
    print('user admin status',admin)
    print('user name is:',user)
    if (signin):
        if(request.method == "POST"):
            item_name = request.form.get("ItemName")
            item_price = request.form.get("ItemPrice")
            effective_from = request.form.get("effectiveFrom")
            try:
                connection.insert_into_items(item_name.title(), item_price,effective_from)
            except Exception as e:
                submitted = "No"
                display_error_message = """We were unable to enter the item to the database. 
                                        Error details:
                                        """+str(e)
                return render_template("admin.html", submitted=submitted,is_admin=admin, display_error_message=display_error_message,user_email=user_email,user_id=user_id,uuser=user)
            submitted = "Yes"
            return render_template("admin.html", submitted=submitted, is_admin=admin,user_email=user_email,user_id=user_id,user=user)

        if ( admin ):
            submitted = "No"
            return render_template("admin.html", submitted=submitted, is_admin=admin,user_email=user_email,user_id=user_id,user=user)
        else:
            return redirect(url_for("create", user_id=user_id))
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
        # if referrer=="https://project-doodh.herokuapp.com/signup": 
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
        db_pwd= connection.get_user_pwd_from_db(user_email,'User')  
        print('db_pwd',db_pwd) 
        if db_pwd=='':
            db_pwd='invalidgooglepwd'  #to handle invalid google login in the login pg
        if (db_pwd==0):
            print('User with this email id has not signed up, please signup')
            display_error_message="User with this email id has not signed up, please signup!"
        elif(sha256_crypt.verify(user_pwd, db_pwd)):
            connection.update_user_signin_status('User',user_id,True)
            print(first_usersigin[user_id])
            if(first_usersigin[user_id]):
                first_usersigin[user_id]=False
                # return redirect(url_for("default",user_id=user_id))
                return redirect(url_for("milkman_selection",user_id=user_id))
            else:
                # we are doing this to make sure it redirects correctly between default and create pages.
                return redirect(url_for("redirect_milkman",user_id=user_id))
            
        else:
            print('Invalid credentials!')
            display_error_message="Invalid credentials!"
    return render_template("signin.html",display_error_message=display_error_message)

@app.route("/signin-success/<social_media_platform>/<user_email>/<user_name>")
def signin_success(social_media_platform, user_email, user_name):
    global first_usersigin
    
    user_id=connection.get_user_id(user_email)
    connection.update_user_signin_status('User',user_id,True)
    user_details=connection.validate_user_signin(user_id) #if a google user signins first time, record for this user wont be inserted into db at this pt in the code, goto connection.py for more clarity on this
    print('in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    referrer=request.referrer
    print('req  is coming from:',referrer)
    #signin status should be true ONLY when on success route comes from signin page, nobody shd manually enter this url and let the insertion of the users happen in the db
    if referrer=="https://project-doodh.herokuapp.com/signin":
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
        
        user_id=connection.get_user_id(user_email)
        connection.update_user_signin_status('User',user_id,True)
        print("count after insert is:",count)
        if count==0:  #first signin shd be set to True only when NEW google user signs in, without this condition it would always set firstsign in to True when google user logs in
            first_usersigin[user_id]=True
        # #function to check if user has entered any default details when they login 1st time, if not then  re-direct them to the default pg again            
        # default_details_count=connection.check_default_details(user_id) 
        # print('user has entered default details? default_details_count:',default_details_count)
        if(first_usersigin[user_id]):            
            first_usersigin[user_id]=False
            # return redirect(url_for("default",user_id=user_id))
            return redirect(url_for("milkman_selection",user_id=user_id))
        else:
            return redirect(url_for("create",user_id=user_id))
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

@app.route('/milkman_selection/<user_id>',methods=["GET","POST"])
def milkman_selection(user_id):
    user_details=connection.validate_user_signin(user_id)
    print('milkman_selection: in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]   
    user=connection.get_user_name(user_email) 
    print('user sign in status',signin)
    print('user admin status',admin)
    print('username is',user)
    if (signin):
        area=None
        city=None  
        # form_data = request.get_json()
        # print('form_data',form_data)   
        # city=form_data
        # print('city',city)
        city=connection.get_milkman_area_city(area,city)
        print('area after connection call:',area)           
        if(request.method == "POST"):  
            print('inside POST user_id:',user_id)
            form_data=request.form 
            # form_data = request.get_json()
            # print('form_data',form_data)
            # area=form_data['area']
            # print('area before connection call:',area)
            city=form_data['city']
            print('city',city)
            area=form_data['area']
            print('area :',area)
            flat_no=form_data['home']
            print('flat_no :',flat_no)
            building=form_data['building']
            print('flat_no :',building)
            address = str(flat_no)+', '+str(building)
            milkman_stores=form_data['milkman_stores']
            print('milkman_stores:',milkman_stores)
            location_id=connection.get_location_id(city,area)
            connection.update_users_with_milkman(milkman_stores,user_id,location_id,address)
            return redirect(url_for("redirect_milkman",user_id=user_id))
            # #function to check if user has entered any default details when they login 1st time, if not then  re-direct them to the default pg again            
            # default_details_count=connection.check_default_details(user_id) 
            # print('user has entered default details? default_details_count:',default_details_count)
            # if (default_details_count==0):
            #  return redirect(url_for("default",user_id=user_id))
            # else:
            #  return redirect(url_for("create",user_id=user_id))  

   
        return  render_template("milkman_selection.html",user_id=user_id,city_list=city,area_list=area,user=user)
        # return city_list
    else:
        return render_template('url_not_found.html')

# This route is used when we skip milkman selection
# This route is also used whenever we need to check if user has added default milk requirements, and based on this we can correctly
# redirect the user to either creaate or default page upon signin
@app.route('/skip_milkman/<user_id>')
def redirect_milkman(user_id):
    #function to check if user has entered any default details when they login 1st time, if not then  re-direct them to the default pg again            
    default_details_count=connection.check_default_details(user_id) 
    print('user has entered default details? default_details_count:',default_details_count)
    if (default_details_count==0):
        return redirect(url_for("default",user_id=user_id))
    else:
        return redirect(url_for("create",user_id=user_id))  


@app.route('/milkman_selection/<user_id>/<city>')
def milkman_selection_area(user_id,city):
    user_details=connection.validate_user_signin(user_id)
    print('milkman_selection:in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):
        # when user selects 'Please select your city' in drop down, we send value City as 'None' string from JavaScript
        # we need to convert the 'None' string to None datatype in python for getmilkman_area_city() logic
        if(city == 'None'):
            city = None
        milkman_area_list=connection.get_milkman_area_city(None,city)
        print(' Area list:')
        pprint(milkman_area_list)
        print('  user_id:',user_id)
    # return render_template("milkman_selection.html",milkman_stores_list=milkman_stores_list,area=area,city=city,user_id=user_id)
        return {'milkman_area_list':milkman_area_list}
    else:
       return render_template('url_not_found.html')       

#same function as above but this will be called in milkman signup page, where milkman_id wont exists so written a separate fucntion excluding milkmanid/userid part from abv function
@app.route('/milkman_signup/<city>')
def milkman_signup_area(city):
  
        milkman_area_list=connection.get_milkman_area_city(None,city)
        print(' Area list:')
        pprint(milkman_area_list)
      
    # return render_template("milkman_selection.html",milkman_stores_list=milkman_stores_list,area=area,city=city,user_id=user_id)
        return {'milkman_area_list':milkman_area_list}
    

@app.route('/milkman_selection/<user_id>/<city>/<area>')
def milkman_selection_stores(user_id,city,area):
    user_details=connection.validate_user_signin(user_id)
    print('StoresList: milkman_selection:in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]    
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):    
        milkman_stores_list=connection.get_milkman_area_city(area,city)
        print(' milkman_stores_list :')
        pprint(milkman_stores_list)
        print('  user_id:',user_id)
    # return render_template("milkman_selection.html",milkman_stores_list=milkman_stores_list,area=area,city=city,user_id=user_id)
        return {'milkman_stores_list':milkman_stores_list}
    else:
       return render_template('url_not_found.html')    

@app.route('/view_milkman/<user_id>/<rating>',methods=["GET","POST"])
def view_milkman(user_id,rating):
    user_details=connection.validate_user_signin(user_id)
    print('milkman_selection:in the server user details:',user_details)
    signin=user_details[0]
    admin=user_details[1]
    user_email=user_details[2]   
    user=connection.get_user_name(user_email) 
    print('user sign in status',signin)
    print('user admin status',admin)
    if (signin):
        city,area,milkman_store=connection.view_user_milkman_details(user_id)
        milkman_list=[milkman_store,area,city]
        print('In server view_milkman():printing the milkman list',milkman_list)
        if city is None and area is None:
            print('Oops no milkman was selected for this user!')
            return render_template('view_modify_milkman.html',user_email=user_email,milkman_list=milkman_list,user_id=user_id,user=user)
        location_id=connection.get_location_id(city,area)
        overall_rate=''
        if rating != ' ':
            milkman_id=connection.milkman_id_store(None,milkman_store, location_id)
            
            connection.milkman_rating(milkman_id,rating,user_id,location_id)
        if milkman_list is not None:
            overall_rate=connection.get_overall_rating(milkman_store,location_id)
        print('overall_rate in server is :',overall_rate) 
        
        return render_template('view_modify_milkman.html',user_email=user_email,milkman_list=milkman_list,user_id=user_id,overall_rate=overall_rate,user=user)
        # city=city,area=area,milkman_store=milkman_store)
    else:
         return render_template('url_not_found.html')

@app.route('/milkman_dashboard/<milkman_id>')
def milkman_dashboard(milkman_id):
    print('MIlkman id is:',milkman_id)
    signed_in=connection.validate_milkman_signin(milkman_id)
    #location id is pased as empty coz if we hv milkman_id without location id we can identify the store uniquely so noeed of loc id
    milkman_store=connection.milkman_id_store(milkman_id,None,'')
    if (signed_in):
        user_count,user_list=connection.milkman_dashboard_logic(milkman_id)
        print('in server user_count:',user_count)
        return render_template('milkman_dashboard.html',user_email='',user_id='',user_count=user_count,user_list=user_list,milkman_id=milkman_id,milkman_store=milkman_store,single_user_list='',address='')
    else:
        return render_template('url_not_found.html')

@app.route('/milkman_dashboard/<milkman_id>/<Social_Media_Name>/<address>')
def milkman_dashboard_single_user(milkman_id,Social_Media_Name,address):
    print('------------milkman_dashboard_single_user-------')
    print('MIlkman id is:',milkman_id)
    print(' Username is:',Social_Media_Name)
    print(' address is:',address)
    signed_in=connection.validate_milkman_signin(milkman_id)
    #location id is pased as empty coz if we hv milkman_id without location id we can identify the store uniquely so no need of loc id
    milkman_store=connection.milkman_id_store(milkman_id,None,'')
    if (signed_in):
        #we need the entire user list to display it in the search customer drop down
        user_count,user_list=connection.milkman_dashboard_logic(milkman_id)
        #we need the single_user_list to display the customer searched by milkman
        user_count,single_user_list=connection.milkman_dashboard_single_user_logic(milkman_id,Social_Media_Name,address)
        print('in server user_count:',user_count)
        print('server: printing the single user list-',single_user_list)
        return render_template('milkman_dashboard.html',user_email='',user_id='',user_count=user_count,user_list=user_list,milkman_id=milkman_id,milkman_store=milkman_store,single_user_list=single_user_list)
    else:
        return render_template('url_not_found.html')


@app.route('/User_Report_Milkman/<milkman_id>/<user_id>/<user>',methods=["GET","POST"])
def User_Report_milkman(milkman_id,user_id,user):
    # user_details=connection.validate_user_signin(user_id)
    print('milkman_id:',milkman_id)
    #location id is pased as empty coz if we hv milkman_id without location id we can identify the store uniquely so noeed of loc id
    milkman_store=connection.milkman_id_store(milkman_id,None,'')
    print('milkman - user_id :',user_id)
    print('milkman - user_name :',user)
    signed_in=connection.validate_milkman_signin(milkman_id)
    if (signed_in):
        if user_id!=0:
            # if user has not provided the month or year
            # find the system month and year
            todays_date = date.today()
            month = int(todays_date.month)
            year = int(todays_date.year)
            month_string = calendar.month_name[month]
            report_list,total_price,tomo_type_qty = connection.report_logic(str(year)+"-"+str(month)+"-01", str(todays_date), user_id)
            
            past_months_list = []
            for i in range(1, 6):
                offset_date = todays_date - DateOffset(months=i)
                past_months_list.append([str(offset_date.month), str(offset_date.year), calendar.month_name[offset_date.month]])
            # past_month_list = [ [3, 2022, March], [2, 2022, February], [1, 2022, January], ... ] considering current_date is in APRIL 2022
            pprint(report_list)
            print (len(report_list))
            print('REPORT TOTAL: ',total_price)

            return render_template("User_Report_Milkman.html", report_list=report_list, month_string=month_string, past_months_list=past_months_list,user_id=user_id,total_price=total_price,user=user,milkman_id=milkman_id,milkman_store=milkman_store)
       
    else:
        return render_template('url_not_found.html')    

@app.route("/milkman/signin",methods = ["GET" , "POST"])
def milkman_signin():
                
    display_error_message=""
    area=None
    city=None 
    city=connection.get_milkman_area_city(area,city) 
    if(request.method == "POST"):
        city = request.form.get("city")
        area = request.form.get("area")
        milkman  = request.form.get("milkman")
        milkman_pwd  = request.form.get("password")

        location_id=connection.get_location_id(city,area)
        milkman_id=connection.milkman_id_store(None,milkman,location_id)
        if milkman_id == 0:
            print('Milkman  has not signed up, please signup')
            area=None
            city=None 
            city=connection.get_milkman_area_city(area,city) 
            display_error_message="Milkman has not signed up, please signup!"
            return render_template("milkman_signin.html",display_error_message=display_error_message,city_list=city,area_list=area)
        print('milkman id while milkman signin is:',milkman_id)
        print('signin',milkman)
        print('signin',milkman_pwd)    
        print('milkman_id',milkman_id)
        db_pwd= connection.get_user_pwd_from_db(milkman_id,'Milkman')
        print('db_pwd',db_pwd) 
        if db_pwd=='':
            db_pwd='invalidgooglepwd'  #to handle invalid google login in the login pg
        if (db_pwd==0):
            print('Milkman  has not signed up, please signup')
            display_error_message="Milkman has not signed up, please signup!"
        elif(sha256_crypt.verify(milkman_pwd, db_pwd)):
            connection.update_user_signin_status('Milkman',milkman_id,True)
           
            return redirect(url_for("milkman_dashboard",milkman_id=milkman_id))   
        else:
            print('Invalid credentials!')
            display_error_message="Invalid credentials!"
    return render_template("milkman_signin.html",display_error_message=display_error_message,city_list=city,area_list=area)

@app.route("/milkman/signup",methods = ["GET", "POST"])
def milkman_signup():
    area=None
    city=None  
    city=connection.get_milkman_area_city(area,city)
    print('area after connection call:',area)      
    if ( request.method== "POST"):
        city = request.form.get("city")
        area = request.form.get("area")
        user_name  = request.form.get("username")
        user_pwd  = request.form.get("password")
        
        print('area and city entered by milkman are: ',area,city)
        print(user_name)
        print(user_pwd)
        user_pwd = sha256_crypt.encrypt(user_pwd)
        print('after hasing',user_pwd)
        count= connection.insert_milkman( user_name, user_pwd,city,area)
        print('the count after calling connection.insert users is:',count)
        location_id=connection.get_location_id(city,area)
        milkman_id=connection.milkman_id_store(None,user_name,location_id)
        print('got the user id in sigup after insert user:',milkman_id)
        if count > 0 :
            submitted = "No"
            display_error_message = """This milkman name already exists in this area! 
                                       Please sign up with a different milkman name. 
                                        """ 
            area=None
            city=None  
            city=connection.get_milkman_area_city(area,city)
            return render_template("milkman_signup.html",submitted=submitted,display_error_message=display_error_message)            
        submitted="Yes" 
        
        return render_template("milkman_signup.html",submitted=submitted,city_list=city,area_list=area)
    submitted="No"
    return render_template("milkman_signup.html",submitted=submitted,city_list=city,area_list=area)

@app.route("/milkman/signout/<milkman>")
def milkman_signout(milkman):
      connection.update_user_signin_status('Milkman',milkman,False)                                         
      return redirect(url_for("milkman_signin"))


if __name__ == "__main__":
    app.run(debug=True)
