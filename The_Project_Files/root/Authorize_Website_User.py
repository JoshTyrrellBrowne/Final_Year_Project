# This file contains route functions for the flask application
# The functions here are for authorizing user details (sign up, login, logout etc)

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from WebDatabases import User
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            if check_password_hash(found_user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(found_user, remember=True)
                return redirect(url_for('usr.home', user=current_user))
            else:
                flash('Incorrect password, try again.', category='error')

        return render_template("login.html", user=current_user)
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("usr.home"), user=current_user)

        return render_template("login.html", user=current_user)


@auth.route("/signUp", methods=["POST", "GET"])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        found_user = User.query.filter_by(email=email).first()

        # Validate the credentials
        if found_user:
            flash('Email already exists.', category='error')
        elif len(email) < 5:
            flash('Email must be greater than 4 characters.', category='error')
            pass
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
            pass
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            pass
        elif len(password1) < 4:
            flash('Password must be greater than 3 characters.', category='error')
            pass
        else:
            # Add user to database
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for("usr.home"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", "info")  # displays the message on webpage
    return redirect(url_for("auth.login", user=current_user))


'''@auth.route("/")
def home():
    return redirect(url_for("auth.login", user=current_user))
'''

