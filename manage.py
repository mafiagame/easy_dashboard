# coding:utf-8

from app import manager, login_db
from app.admin_models import User


@manager.command
def create_new_user(email, password):
    user = User()
    user.email = email
    user.username = email.split("@")[0]
    user.password = password
    login_db.session.add(user)
    login_db.session.commit()

if __name__ == "__main__":
    manager.run()