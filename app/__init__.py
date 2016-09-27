from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis
app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)
mail = Mail(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

from controller.main import *