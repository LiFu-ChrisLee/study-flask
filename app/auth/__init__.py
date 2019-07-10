# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 18:03
# @Author  : Li Fu

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
