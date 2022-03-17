from operator import methodcaller
from flask import Flask, render_template, redirect, request, url_for
import connection


app = Flask(__name__, template_folder='../templates', static_folder="../static")

@app.route("/")
def redirect_to_create():
    return redirect(url_for("signin"))
    # this will redirect to the signin() python function

@app.route("/create",methods = ["GET", "POST"])
def create():
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
        return render_template("create.html", submitted=submitted)
    submitted = "No"            
    return render_template("create.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/default")
def create_default():
    return render_template("default.html")

@app.route("/items", methods = ["GET", "POST"])
def items():
    if(request.method == "POST"):
        item_name = request.form.get("ItemName")
        item_price = request.form.get("ItemPrice")
        connection.insert_into_items(item_name, item_price)
        submitted = "Yes"
        return render_template("admin.html", submitted=submitted)
    # item = connection.connect()
    # return (str(item))
    submitted = "No"
    return render_template("admin.html", submitted=submitted)

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signin-success/<social_media_platform>/<user_email>/<user_name>")
def signin_success(social_media_platform, user_email, user_name):
    connection.insert_users(user_email, user_name, social_media_platform)
    return redirect(url_for("create"))

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)