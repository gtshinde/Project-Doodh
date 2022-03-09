from multiprocessing import connection
from sqlite3 import connect
from flask import Flask, render_template, redirect, url_for
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

@app.route("/items")
def items():
    (item, price) = connection.connect()
    return (str(item)+str(price))

@app.route("/signin")
def signin():
    return render_template("signin.html")

if __name__ == "__main__":
    app.run(debug=True)