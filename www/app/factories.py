#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-06 01:25:33
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 1

import logging
import json
from aiohttp import web
from urllib import parse

from app import COOKIE_NAME
from app.models import User
# -------------------------工厂函数------------------------------------
# 在每个响应之前打印日志
async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Response: %s %s' % (request.method, request.path))
        return await handler(request)
    return logger

# 通过cookie找到当前用户信息，把用户绑定在request.__user__
async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        cookie = request.cookies.get(COOKIE_NAME)
        request.__user__ = await User.find_by_cookie(cookie)
        if request.__user__ is not None:
            logging.info('set current user: %s' % request.__user__.email)
        return await handler(request)
    return auth

async def data_factory(app, handler):
    async def parse_data(request):
        logging.info('data_factory...')
        if request.method in ('POST', 'PUT'):
            if not request.content_type:
                return web.HTTPBadRequest(text='Missing Content-Type.')
            content_type = request.content_type.lower()
            if content_type.startswith('application/json'):
                request.__data__ = await request.json()
                if not isinstance(request.__data__, dict):
                    return web.HTTPBadRequest(text='JSON body must be object.')
                logging.info('request json: %s' % request.__data__)
            elif content_type.startswith(('application/x-www-form-urlencoded', 'multipart/form-data')):
                params = await request.post()
                request.__data__ = dict(**params)
                logging.info('request form: %s' % request.__data__)
            else:
                return web.HTTPBadRequest(text='Unsupported Content-Type: %s' % content_type)
        elif request.method == 'GET':
            qs = request.query_string
            request.__data__ = {k: v[0] for k, v in parse.parse_qs(qs, True).items()}
            logging.info('request query: %s' % request.__data__)
        else:
            request.__data__ = dict()
        return await handler(request)
    return parse_data

# 把任何返回值封装成浏览器可正确显示的Response对象
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                # 如果用jinja2渲染，绑定已验证过的用户
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and 100 <= r < 600:
            return web.Response(status=r)
        if isinstance(r, tuple) and len(r) == 2:
            status, message = r
            if isinstance(status, int) and 100 <= status < 600:
                return web.Response(status=status, text=str(message))
        # default
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response
