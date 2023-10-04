from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash, gen_salt

db = SQLAlchemy()

class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.Integer, index=True, unique=True)
    serial = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    make = db.Column(db.String(64), index=True)

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