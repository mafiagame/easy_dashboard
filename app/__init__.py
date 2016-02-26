# coding:utf-8

# coding:utf-8
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_moment import Moment

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MONGODB_DB'] = 'battlefield'
app.config['CSRF_ENABLED'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.debug = True
bootstrap = Bootstrap(app)
moment = Moment(app)
login_db = SQLAlchemy(app)
login_manager = LoginManager(app)
manager = Manager(app)

from app import views, models
