# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 11:20
# @Author  : Li Fu


from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# send mail
def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
    thr = Thread(target=send_async_email, args=[current_app, msg])
    thr.start()
    return thr
