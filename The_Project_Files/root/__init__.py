import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# from WebDatabases import User, Currency    # this is my own script for defining databases

# from Graphs import getHTMLStringOfGraph, getTest
# from GetHistoricalDataBinance import get_eth_usd_graph

db = SQLAlchemy()
DB_NAME = "usersDatabase.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = "joshbrowneSecretKey468468168749"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.permanent_session_lifetime = timedelta(minutes=60)

    from Authorize_Website_User import auth
    app.register_blueprint(auth, url_prefix='/')  # set the blueprint connection app -> auth

    from User_WebPages import usr
    app.register_blueprint(usr, url_prefix='/')

    from WebDatabases import User

    db.init_app(app)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists('scripts/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

