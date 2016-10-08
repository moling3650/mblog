#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-28 19:26:23
# @Author  : moling (365024424@qq.com)
# @Link    : http://www.qiangtaoli.com
# @Version : 2
import logging

from app.frame import get, post, put, delete
from app.frame.halper import Page, set_valid_value, check_user, check_string
from app.frame.errors import APIResourceNotFoundError
from app.models import User, Blog, Comment

URL_PREFIX = '/api/v2.0'


# 获取表（用户、博客、评论）一页的条目
@get(URL_PREFIX + '/{table}')
async def api_get_items_v2(table, *, page='1', size='10'):
    models = {'users': User, 'blogs': Blog, 'comments': Comment}
    num = await models[table].countRows()
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        return dict(page=page, items=[])
    items = await models[table].findAll(orderBy='created_at desc', limit=(page.offset, page.limit + num % page.limit))
    return dict(page=page, items=[item.to_json(encrypted=True) for item in items])


# 创建一个博客
@post(URL_PREFIX + '/blog/')
async def api_create_blog_v2(request, *, name, summary, content):
    check_user(request.__user__)
    check_string(name=name, summary=summary, content=content)
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog.to_json()


# 获取一个博客
@get(URL_PREFIX + '/blog/{id}')
async def api_get_blog_v2(id):
    blog = await Blog.find(id)
    return blog.to_json()


# 修改一个博客
@put(URL_PREFIX + '/blog/{id}')
async def api_update_blog_v2(id, request, *, name, summary, content):
    check_user(request.__user__)
    check_string(name=name, summary=summary, content=content)
    blog = await Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog.to_json()


# 从表（用户，博客，评论）删除一个元素
@delete(URL_PREFIX + '/{table}/{id}')
async def api_delete_item_v2(table, id, request):
    models = {'user': User, 'blog': Blog, 'comment': Comment}
    check_user(request.__user__)
    item = await models[table].find(id)
    if item:
        await item.remove()
    else:
        logging.warn('id: %s not exist in %s' % (id, table))
    return dict(id=id)


# 获取一篇博客的所有评论
@get(URL_PREFIX + '/blog/{id}/comments')
async def api_get_blog_comments_v2(id):
    comments = await Comment.findAll('blog_id = ?', [id], orderBy='created_at desc')
    return dict(comments=[c.to_json(marked=True) for c in comments])


# 创建一个评论
@post(URL_PREFIX + '/blog/{id}/comment')
async def api_create_comment_v2(id, request, *, content, time):
    user = request.__user__
    check_user(user, check_admin=False)
    check_string(content=content)
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image, content=content.lstrip('\n').rstrip())
    await comment.save()
    comments = await Comment.findAll('blog_id = ? and created_at > ?', [id, time], orderBy='created_at desc')
    return dict(comments=[c.to_json(marked=True) for c in comments])
