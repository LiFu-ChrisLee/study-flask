# -*- coding: utf-8 -*-
# @Time    : 2019/7/8 14:40
# @Author  : Li Fu

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
