#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 22:51:06
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
from app.frame import get
from app.frame.halper import Page, set_valid_value
from app.models import Blog


# 测试
@get('/about')
async def about():
    return {
        '__template__': 'about.html'
    }


# 首页
@get('/')
async def index():
    return 'redirect:/bootstrap/'


@get('/{template}/')
async def home(template, *, tag='', page='1', size='10'):
    num = await Blog.countRows(where="position(? in `summary`)", args=[tag])
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll("position(? in `summary`)", [tag], orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': '%s-blogs.html' % (template),
        'blogs': blogs,
        'page': page,
        'tag': tag
    }


# 注册页面
@get('/{template}/register')
def register(template):
    return {
        '__template__': '%s-register.html' % (template)
    }


# 登陆页面
@get('/{template}/signin')
def signin(template):
    return {
        '__template__': '%s-signin.html' % (template)
    }


# 博客页面
@get('/{template}/blog/{id}')
async def get_bolg(template, id):
    blog = await Blog.find(id)
    return {
        '__template__': '%s-blog.html' % (template),
        'blog': blog
    }


# 管理页面
@get('/{template}/manage')
def manage(template):
    return 'redirect:/%s/manage/blogs' % (template)


# 管理用户、博客、评论
@get('/{template}/manage/{table}')
def manage_table(template, table):
    return {
        '__template__': '%s-manage.html' % (template),
        'table': table
    }


# 创建博客
@get('/{template}/manage/blogs/create')
def manage_create_blog(template):
    return {
        '__template__': '%s-blog_edit.html' % (template)
    }


# 修改博客
@get('/{template}/manage/blogs/edit')
def manage_edit_blog(template):
    return {
        '__template__': '%s-blog_edit.html' % (template)
    }


# 谷歌验证
@get('/google8d8dd87f7b70fbc7.html')
def google_auth():
    return {
        '__template__': 'google8d8dd87f7b70fbc7.html'
    }
