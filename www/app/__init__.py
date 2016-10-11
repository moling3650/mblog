#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 14:32:46
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
import logging
import os
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from config import COOKIE_NAME, COOKIE_KEY
from app.frame import add_routes, add_static
from app.frame.orm import create_pool
from app.factories import logger_factory, auth_factory, data_factory, response_factory
from app.filters import datetime_filter, marked_filter

logging.basicConfig(level=logging.INFO)


# jinja2初始化函数
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = {
        'autoescape': kw.get('autoescape', True),
        'block_start_string': kw.get('block_start_string', '{%'),
        'block_end_string': kw.get('block_end_string', '%}'),
        'variable_start_string': kw.get('variable_start_string', '{{'),
        'variable_end_string': kw.get('variable_end_string', '}}'),
        'auto_reload': kw.get('auto_reload', True)
    }
    path = kw.get('path', os.path.join(__path__[0], 'templates'))
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters')
    if filters is not None:
        for name, ftr in filters.items():
            env.filters[name] = ftr
    app['__templating__'] = env


async def create_server(loop, config_mod_name):
    try:
        config = __import__(config_mod_name, fromlist=['get config'])
    except ImportError as e:
        raise e

    await create_pool(loop, **config.db_config)
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, data_factory, response_factory])
    add_routes(app, 'app.route')
    add_routes(app, 'app.api')
    add_routes(app, 'app.api_v2')
    add_static(app)
    init_jinja2(app, filters=dict(datetime=datetime_filter, marked=marked_filter), **config.jinja2_config)
    server = await loop.create_server(app.make_handler(), '127.0.0.1', 9900)
    logging.info('server started at http://127.0.0.1:9900...')
    return server
