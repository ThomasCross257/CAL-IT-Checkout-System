from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Admin {}>'.format(self.username)