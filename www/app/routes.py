#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 22:51:06
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
#
from app.frame import get, post
from app.frame.halper import Page, get_page_index
from app.models import User, Blog, Comment
from aiohttp import web


@get('/')
async def index(*, page='1'):
    num = await Blog.countRows('id')
    page_info = Page(num, get_page_index(page))
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(page_info.offset, page_info.limit))
    return {
        '__template__': 'blogs.html',
        'page': page_info,
        'blogs': blogs
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