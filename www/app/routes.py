#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 22:51:06
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
#
from app.frame import get, post
from app.models import User
from aiohttp import web

@get('/')
async def index():
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }

@get('/404')
def not_found():
    return 404

@get('/json')
def get_json():
    return dict(name='json', version='1.0')

@get('/hi/{name}')
def say_hi(name):
    return 'Hi %s' % name