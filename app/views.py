# coding:utf-8
import json
from pprint import pprint
from app import app, login_manager
from app.admin_models import User
from app.forms import LoginForm
from app.models import Player
from app.utils import *
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you have been logged out")
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/player-info")
@login_required
def player_info():
    single_form_fields = create_single_form_fields()
    double_level_fields = create_double_level_fields()
    return render_template("player-info.html", single_form_fields=single_form_fields, double_level_fields=double_level_fields)


@app.route("/player-search-name", methods=["GET", "POST"])
@login_required
def player_search_name():
    if request.method == "GET":
        player_name = request.args.get('name')
        # player = Player.player_test()
        player = Player.player_find_by_name(player_name)
        if not player:
            return ""
        return JSONEncoder().encode(player)
    else:
        player_data = json.loads(request.data)
        # 预处理player变量 纠正变量类型
        adjust_player_data(player_data)
        Player.player_find_and_replace_by_id(player_data["_id"], player_data)
        return "1"
