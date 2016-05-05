#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 14:32:46
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
import logging
from aiohttp import web
from .frame import add_routes, add_static

logging.basicConfig(level=logging.INFO)

async def create_server(loop):

    app = web.Application(loop=loop)
    add_routes(app, 'app.routes')
    add_static(app)
    server = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return server