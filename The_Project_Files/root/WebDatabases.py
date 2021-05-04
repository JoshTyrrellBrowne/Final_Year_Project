from flask_login import UserMixin
from sqlalchemy.sql import func
from __init__ import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    currencies = db.relationship('Currency')


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'))  # many to one link between databases, each of these is connected to 1 user (notice 'user' is lowercase)
    name = db.Column(db.String(20))
