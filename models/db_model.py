from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Integer, nullable=False)
    serial = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    make = db.relationship('Make', backref=db.backref('laptops', lazy=True))

class CheckedOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptop.id'), nullable=False)
    user_fname = db.Column(db.String(50))
    user_lname = db.Column(db.String(50))
    user_coyoteID = db.Column(db.Integer)
    user_address = db.Column(db.String(100))
    checked_out_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, default=False)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    password_salt = db.Column(db.String(50), nullable=False)