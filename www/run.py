#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 14:28:27
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import asyncio
from app import create_server

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_server(loop))
    loop.run_forever()