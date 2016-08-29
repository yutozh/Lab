# coding=utf8

from app import db
from flask.ext.sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=False)
    bookInfo = db.Column(db.String(128),unique=False)
    email = db.Column(db.String(128))