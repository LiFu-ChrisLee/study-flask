# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 15:06
# @Author  : Li Fu

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# form validate
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
