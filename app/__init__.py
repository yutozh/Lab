from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import redis
app = Flask(__name__)

app.config.from_object("config")

db = SQLAlchemy(app)
mail = Mail(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
if not r.exists('PV'):
    r.set('PV',0)
if not r.exists('SUCCESS'):
    r.set('SUCCESS', 0)
if not r.exists('ALL'):
    r.set('ALL', 0)

from controller.main import *