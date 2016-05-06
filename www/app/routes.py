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
from app.frame.halper import *
from app.frame.errors import APIValueError, APIPermissionError, APIResourceNotFoundError
from app.frame.markdown2 import markdown
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
    user = User(name=name.strip(), email=email, password=password, image='/static/img/user.png')
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

@get('/blog/{id}')
async def get_bolg(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id = ?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }

@get('/api/blogs/{id}')
async def api_get_blog(id):
    return await Blog.find(id)

@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.strip())
    await comment.save()
    return comment

# 管理页面
@get('/manage')
def manage():
    return 'redirect:/manage/blogs'

@get('/manage/{table}')
def manage_table(table, *, page='1'):
    return {
        '__template__': 'manage_%s.html' % table,
        'page_index': get_page_index(page)
    }

@get('/api/{table}')
async def api_model(table, *, page=1):
    models = {'users': User, 'blogs': Blog, 'comments': Comment}
    num = await models[table].countRows('id')
    page_info = Page(num, get_page_index(page))
    if num == 0:
        return { 'page': page_info, table: () }
    items = await models[table].findAll(orderBy='created_at desc', limit=(page_info.offset, page_info.limit))
    return { 'page': page_info, table: items }

# 创建博客
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }

@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    check_string(name=name, summary=summary, content=content)
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                        name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog

# 更改或删除博客
@get('/manage/blogs/edit')
def manage_edit_blog(id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }

@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    check_string(name=name, summary=summary, content=content)
    blog = await Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog

@post('/api/{table}/{id}/delete')
async def api_delete_item(table, id, request):
    models = {'blogs': Blog, 'comments': Comment}
    check_admin(request)
    item = await models[table].find(id)
    if item:
        await item.remove()
    else:
        logging.warn('id: %s not exist in %s' %(id, table))
    if table == 'blogs':
        comments = await Comment.findAll('blog_id = ?', [id])
        for comment in comments:
            await comment.remove()
    return dict(id=id)