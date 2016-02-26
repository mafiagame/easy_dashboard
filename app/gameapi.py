# coding:utf-8


def send_announce_to_players(title, content):
    from model.mail import Mail
    Mail.send_system_all_mail(title, {'txt': content})