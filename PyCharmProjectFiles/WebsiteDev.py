from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
# from Graphs import getHTMLStringOfGraph, getTest
from GetHistoricalDataBinance import get_eth_usd_graph

app = Flask(__name__)
app.secret_key = "joshbrowneSecretKey420"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=60)

db = SQLAlchemy(app)

# graphHTML = ""
# getHTMLStringOfGraph(graphHTML)
#  session["graphHTML"] = graphHTML

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("example.html")
    #  return "Hello! this is the main page."

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        userName = request.form["nm"]
        session["userName"] = userName

        found_user = users.query.filter_by(name=userName).first()
        #  users.query.filter_by(name=userName).delete() ...to delete
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(userName, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "userName" in session:
        userName = session["userName"]

        if request.method == "POST":
            email = request.form["email"]
            found_user = users.query.filter_by(name=userName).first()
            found_user.email = email
            session["email"] = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        plot_url = get_eth_usd_graph()

        return render_template("user.html", userName=userName, email=email, plot_url=plot_url)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out!", "info")  # displays the message on webpage
    return redirect(url_for("login"))

if __name__  ==  "__main__":
    db.create_all()  # this creates the database if one does not yet exist
    app.run(debug=True)
