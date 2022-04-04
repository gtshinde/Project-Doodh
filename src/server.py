# from operator import methodcaller
# from crypt import methods
from operator import is_
from re import sub
from flask import Flask, render_template, redirect, request, url_for
import connection

is_admin = False
user_email_val = '' 

app = Flask(__name__, template_folder='../templates', static_folder="../static")

@app.route("/")
def redirect_to_create():
    return redirect(url_for("signin"))
    # this will redirect to the signin() python function

@app.route("/create",methods = ["GET", "POST"])
def create():
    global is_admin
    if (request.method == "POST"):
        item_id = 1
        item_qty = request.form.get("cm")
        if (item_qty != '0.0'):
            connection.insert_into_change(item_id, item_qty)  
        item_id = 2
        item_qty = request.form.get("bm")
        if (item_qty != '0.0'):
            connection.insert_into_change(item_id, item_qty)  
        submitted = "Yes"
        return render_template("create.html", submitted=submitted, is_admin=is_admin)
    submitted = "No" 
    print(str(is_admin)+' before create')           
    return render_template("create.html",is_admin=is_admin)

@app.route("/report")
def report():
    return render_template("report.html",is_admin=is_admin)

@app.route("/default", methods=["GET", "POST"])
def create_default():
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
    return render_template("default.html", is_admin=is_admin)

@app.route("/items", methods = ["GET", "POST"])
def items():
    global user_email_val
    is_admin = connection.is_admin(user_email_val)
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
            return render_template("admin.html", submitted=submitted, display_error_message=display_error_message)
        submitted = "Yes"
        return render_template("admin.html", submitted=submitted, is_admin=is_admin)
    # item = connection.connect()
    # return (str(item))

    print(is_admin) 
    if ( is_admin == True ):
        submitted = "No"
        return render_template("admin.html", submitted=submitted, is_admin=is_admin)
    else:
        return redirect(url_for("create"))

@app.route("/signin")
def signin():
    global is_admin 
    is_admin = False
    return render_template("signin.html")

@app.route("/signin-success/<social_media_platform>/<user_email>/<user_name>")
def signin_success(social_media_platform, user_email, user_name):
    global is_admin
    global user_email_val 
    print(social_media_platform)
    print(user_email)
    print(user_name)
    user_email_val = user_email 
    connection.insert_users(user_email, user_name, social_media_platform)
    # return redirect(url_for("create"))
    is_admin = connection.is_admin(user_email)
    print(is_admin) 
    return redirect(url_for("create"))
    # return render_template("create.html",isadmin=isadmin)

@app.route("/signup",methods = ["GET", "POST"])
def signup():
    if ( request.method== "POST"):
        user_email = request.form.get("email")
        user_name  = request.form.get("username")
        social_media_platform = ''
        count= connection.insert_users(user_email, user_name, social_media_platform)
        if count > 0 :
            submitted = "No"
            display_error_message = """This email id already exists into the database. 
                                        """ 
            return render_template("signup.html",submitted=submitted,display_error_message=display_error_message)           
        # return redirect(url_for("create"))
        is_admin = connection.is_admin(user_email)
        print(is_admin)  
        submitted="Yes"   
        return render_template("signup.html",submitted=submitted)
    submitted="No"
    return render_template("signup.html",submitted=submitted)

if __name__ == "__main__":
    app.run(debug=True)