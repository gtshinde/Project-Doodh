from flask import Flask, render_template, redirect, request, url_for
import connection


app = Flask(__name__, template_folder='../templates', static_folder="../static")

@app.route("/")
def redirect_to_create():
    return redirect(url_for("create"))
    # this will redirect to the create() python function

@app.route("/create")
def create():
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
        return "Added into the database! (Hopefully)"
    # item = connection.connect()
    # return (str(item))
    return render_template("admin.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

if __name__ == "__main__":
    app.run(debug=True)