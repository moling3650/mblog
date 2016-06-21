#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 19:40:23
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1

db_config = {
    'user': 'moling',
    'password': 'www-data',
    'db': 'mblog'
}

jinja2_config = dict()

COOKIE_NAME = 'aweSession'
COOKIE_KEY = 'MbLog'

__all__ = ['db_config', 'jinja2_config', 'COOKIE_NAME', 'COOKIE_KEY']
