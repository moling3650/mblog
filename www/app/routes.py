#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 22:51:06
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
#
from .frame import get, post
from aiohttp import web

@get('/')
def index():
    return web.Response(body=b'<h1>hello world</h1>')