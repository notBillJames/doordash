from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    dashses = db.relationship('Dashes')
    orders = db.relationship('Orders')


class PendingOrders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    distance = db.Column(db.Integer)
    pay = db.Column(db.Integer)
    accept_time = db.Column(db.DateTime(timezone=True))
    pickup_time = db.Column(db.DateTime(timezone=True))
    dropoff_time = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer)
    dash_id = db.Column(db.Integer)


class Dashes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime(timezone=True))
    end = db.Column(db.DateTime(timezone=True))
    location = db.Column(db.String(150))
    promo = db.Column(db.Integer, default=0)
    total_pay = db.Column(db.Integer)
    gas_cost = db.Column(db.Integer)
    total_miles = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    orders = db.relationship('Orders')


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    distance = db.Column(db.Integer)
    pay = db.Column(db.Integer)
    accept_time = db.Column(db.DateTime(timezone=True))
    pickup_time = db.Column(db.DateTime(timezone=True))
    dropoff_time = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dash_id = db.Column(db.Integer, db.ForeignKey('dashes.id'))
