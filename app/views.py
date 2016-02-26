# coding:utf-8
from datetime import datetime
import json
from pprint import pprint
from app import app, login_manager, login_db
from app.admin_models import User, Announce, Compensate
from app.forms import LoginForm
from app.models import Player
from app.gameapi import *
from app.utils import *
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user


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
        return ""


@app.route("/player-single-save", methods=["POST"])
@login_required
def player_single_save():
    data = json.loads(request.data)
    adjust_single_data(data)
    Player.player_update_single_field(data)
    player = Player.player_find_by_id(data["_id"])
    return JSONEncoder().encode(player)


@app.route("/player-building-save", methods=["POST"])
@login_required
def player_building_save():
    data = json.loads(request.data)
    data["_id"] = ObjectId(data["_id"])
    data["building_lv"] = int(data["building_lv"])
    Player.collection.update_one({"_id": data["_id"]}, {"$set": {"buildings.%s.level" % data["building_pos"]: data["building_lv"]}})
    player = Player.player_find_by_id(data["_id"])
    return JSONEncoder().encode(player)


@app.route("/announce-info")
@login_required
def announce_info():
    page = request.args.get('page', 1, type=int)
    pagination = Announce.query.order_by(Announce.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    announces = pagination.items
    return render_template("announcement.html", announces=announces, pagination=pagination)


@app.route("/announce-send", methods=["POST"])
@login_required
def announce_send():
    data = json.loads(request.data)
    # send_announce_to_players(data["announce_title"], data["announce_content"])
    announce = Announce(title=data["announce_title"], content=data["announce_content"], author_id=current_user.id)
    login_db.session.add(announce)
    login_db.session.commit()

    return ""


@app.route("/compensate-info")
@login_required
def compensate_info():
    page = request.args.get('page', 1, type=int)
    pagination = Compensate.query.order_by(Compensate.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    compensates = pagination.items

    return render_template("compensate-info.html", compensates=compensates, pagination=pagination)


@app.route("/compensate-send", methods=["POST"])
@login_required
def compensate_send():
    data = json.loads(request.data)
    Player.player_compensate(data)
    compensate = Compensate(comment=data["comment"], content=request.data, author_id=current_user.id)
    login_db.session.add(compensate)
    login_db.session.commit()

    return ""