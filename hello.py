# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 2:37
# @Author  : Li Fu

import os

import json

from flask import Flask, render_template, session, redirect, url_for

from flask_bootstrap import Bootstrap

from flask_moment import Moment

from flask_script import Shell, Manager

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand

from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# security key for form
app.config['SECRET_KEY'] = 'hard to guess string'

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# mail config
with open('../env.json') as file:
    env_json_str = file.read()
    env = json.loads(env_json_str)
app.config['MAIL_SERVER'] = env['MAIL_SERVER']
app.config['MAIL_USERNAME'] = env['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = env['MAIL_PASSWORD']
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <%s@%s>' % (
    env['MAIL_USERNAME'], '.'.join(env['MAIL_SERVER'].split('.')[1:]))
app.config['FLASKY_ADMIN'] = '%s@%s' % (env['MAIL_USERNAME'], '.'.join(env['MAIL_SERVER'].split('.')[1:]))

# bootstrap
bootstrap = Bootstrap(app)

# moment
moment = Moment(app)

# orm
db = SQLAlchemy(app)

# shell command
manager = Manager(app)

# db migrate
migrate = Migrate(app, db)

# mail
mail = Mail(app)


# db model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


# db model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


# form validate
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# shell command
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


# send mail
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


# routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        input_user = User.query.filter_by(username=form.name.data).first()
        if input_user is None:
            input_user = User(username=form.name.data)
            db.session.add(input_user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=input_user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    # shell command
    # manager.run()
    app.run(debug=True)
