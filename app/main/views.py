# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 14:43
# @Author  : Li Fu

from flask import render_template, session, redirect, url_for
from datetime import datetime
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False),
                           current_time=datetime.utcnow())
