from flask import Flask, render_template, redirect, url_for

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

if __name__ == "__main__":
    app.run(debug=True)