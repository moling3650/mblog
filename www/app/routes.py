#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 22:51:06
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1

import hashlib, json, logging, re
from aiohttp import web

from app import COOKIE_NAME
from app.frame import get, post
from app.frame.halper import Page, get_page_index
from app.frame.errors import APIValueError
from app.models import User, Blog, Comment

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

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
    return {
        '__template__': '404.html'
    }

# 注册一个新用户
@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }

@post('/api/register')
async def api_register_user(*, email, name, password):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    users = await User.findAll('email = ?', [email])
    if len(users) > 0:
        raise ('register:failed', 'email', 'Email is already in use.')
    user = User(name=name.strip(), email=email, password=password, image='empty')
    await user.register()
    # make session cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user.generate_cookie(86400), max_age=86400, httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 用户登陆
@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }

@post('/api/authenticate')
async def authenticate(*, email, password):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not password:
        raise APIValueError('password', 'Invalid password.')
    users = await User.findAll('email = ?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check password
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(password.encode('utf-8'))
    if user.password != sha1.hexdigest():
        raise APIValueError('password', 'Invalid password')
    # authenticate ok, set cookie
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user.generate_cookie(86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 注销用户
@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    # 清理掉cookie得用户信息数据
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out')
    return r