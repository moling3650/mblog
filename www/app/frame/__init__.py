#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 22:14:44
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1

import asyncio
import functools
import inspect
import logging
import os
from aiohttp import web

from .errors import APIError


def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


class RequestHandler(object):

    def __init__(self, func):
        self._func = func

    async def __call__(self, request):
        # 获取函数的参数表
        required_args = inspect.signature(self._func).parameters
        logging.info('required args: %s' % required_args)

        # 获取从GET或POST传进来的参数值，如果函数参数表有这参数名就加入
        kw = {arg: value for arg, value in request.__data__.items() if arg in required_args}

        # 获取match_info的参数值，例如@get('/blog/{id}')之类的参数值
        kw.update(dict(**request.match_info))

        # 如果有request参数的话也加入
        if 'request' in required_args:
            kw['request'] = request

        # 检查参数表中有没参数缺失
        for key, arg in required_args.items():
            # request参数不能为可变长参数
            if key == 'request' and arg.kind in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                return web.HTTPBadRequest(text='request parameter cannot be the var argument.')
            # 如果参数类型不是变长列表和变长字典，变长参数是可缺省的
            if arg.kind not in (arg.VAR_POSITIONAL, arg.VAR_KEYWORD):
                # 如果还是没有默认值，而且还没有传值的话就报错
                if arg.default == arg.empty and arg.name not in kw:
                    return web.HTTPBadRequest(text='Missing argument: %s' % arg.name)

        logging.info('call with args: %s' % kw)
        try:
            return await self._func(**kw)
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)


# 添加一个模块的所有路由
def add_routes(app, module_name):
    try:
        mod = __import__(module_name, fromlist=['get_submodule'])
    except ImportError as e:
        raise e

    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        func = getattr(mod, attr)
        if callable(func):
            method = getattr(func, '__method__', None)
            path = getattr(func, '__route__', None)
            if method and path:
                func = asyncio.coroutine(func)
                args = ', '.join(inspect.signature(func).parameters.keys())
                logging.info('add route %s %s => %s(%s)' % (method, path, func.__name__, args))
                app.router.add_route(method, path, RequestHandler(func))


# 添加静态文件夹的路径
def add_static(app):
    path = os.path.join(os.path.dirname(__path__[0]), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))
