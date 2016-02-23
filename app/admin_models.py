# coding:utf-8

from app import login_db
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, login_db.Model):
    __tablename__ = "users"
    id = login_db.Column(login_db.Integer, primary_key = True)
    email = login_db.Column(login_db.String(64), unique=True, index=True)
    username = login_db.Column(login_db.String(64), unique=True, index=True)
    password_hash = login_db.Column(login_db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
