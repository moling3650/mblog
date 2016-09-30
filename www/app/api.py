#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-26 02:46:05
# @Author  : moling (365024424@qq.com)
# @Link    : http://www.qiangtaoli.com
# @Version : $Id$
import logging
from aiohttp import ClientSession, web

from app.filters import marked_filter as markdown_highlight
from app.frame import get, post
from app.frame.halper import Page, set_valid_value, check_user, check_string, check_email_and_password
from app.frame.errors import APIValueError, APIResourceNotFoundError
from app.models import User, Blog, Comment, Oauth


# 注册新用户
@post('/register')
async def register(*, name, email, sha1_pw, oid=None, image=None):
    check_string(name=name)
    check_email_and_password(email, sha1_pw)
    users = await User.findAll('email = ?', [email])
    if users:
        raise APIValueError('email', 'Email is already in used.')
    user = User(name=name.strip(), email=email, password=sha1_pw, image=image or '/static/img/user.png')
    await user.save()
    if oid:
        o = Oauth(id=oid, user_id=user.id)
        await o.save()
    # register ok, signin
    return user.signin(web.json_response({'signin user': user.name}))


# 登陆验证
@post('/authenticate')
async def authenticate(*, email, sha1_pw):
    check_email_and_password(email, sha1_pw)
    users = await User.findAll('email = ?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check password
    if not user.verify_password(sha1_pw):
        raise APIValueError('password', 'Invalid password')
    # authenticate ok, signin
    return user.signin(web.json_response({'signin user': user.name}))


@get('/oauth2')
async def oauth2(code):
    url = 'https://api.weibo.com/oauth2/access_token'
    payload = {
        'client_id': '366603916',
        'client_secret': 'b418efbd77094585d0a7f9ccac98a706',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://www.qiangtaoli.com'
    }
    with ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            params = await resp.json()
        async with session.get('https://api.weibo.com/2/users/show.json', params=params) as resp:
            info = await resp.json()
        o = await Oauth.find('weibo-' + info['idstr'])
        if not o:
            return 'redirect:/bootstrap/register?oid=weibo-%s&name=%s&image=%s' % (info['idstr'], info['name'], info['avatar_large'])
        user = await User.find(o.user_id)
        if not user:
            return 'oauth user was deleted.'
        return user.signin(web.HTTPFound('/'))


# 注销用户
@get('/signout')
def signout(request):
    logging.info('user sign out')
    return User.signout(web.HTTPFound(request.headers.get('Referer') or '/'))


# 取（用户、博客、评论）表的条目
@get('/api/{table}')
async def api_get_items(table, *, page='1', size='10'):
    models = {'users': User, 'blogs': Blog, 'comments': Comment, 'oauth': Oauth}
    num = await models[table].countRows()
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        return dict(page=page, items=[])
    items = await models[table].findAll(orderBy='created_at desc', limit=(page.offset, page.limit + num % page.limit))
    if table == 'users':
        for user in items:
            user.password = '******'
    return dict(page=page, items=items)


# 取某篇博客
@get('/api/blogs/{id}')
async def api_get_blog(id):
    return await Blog.find(id)


# 创建新博客
@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_user(request.__user__)
    check_string(name=name, summary=summary, content=content)
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


# 修改某篇博客
@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_user(request.__user__)
    check_string(name=name, summary=summary, content=content)
    blog = await Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


# 取某篇博客的所有评论
@get('/api/blogs/{id}/comments')
async def api_get_blog_comments(id):
    comments = await Comment.findAll('blog_id = ?', [id], orderBy='created_at desc')
    for c in comments:
        c.content = markdown_highlight(c.content)
    return dict(comments=comments)


# 创建新评论
@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content, time):
    user = request.__user__
    check_user(user, check_admin=False)
    check_string(content=content)
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.lstrip('\n').rstrip())
    await comment.save()
    comments = await Comment.findAll('blog_id = ? and created_at > ?', [id, time], orderBy='created_at desc')
    for c in comments:
        c.content = markdown_highlight(c.content)
    return dict(comments=comments)


# 删除博客或评论
@post('/api/{table}/{id}/delete')
async def api_delete_item(table, id, request):
    models = {'users': User, 'blogs': Blog, 'comments': Comment, 'oauth': Oauth}
    check_user(request.__user__)
    item = await models[table].find(id)
    if item:
        await item.remove()
    else:
        logging.warn('id: %s not exist in %s' % (id, table))
    return dict(id=id)
