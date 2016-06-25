#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 14:28:27
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
import asyncio
from app import create_server

if __name__ == '__main__':
    # 创建一个异步事件回路实例
    loop = asyncio.get_event_loop()
    # 创建一个服务器实例放入到异步事件回路
    loop.run_until_complete(create_server(loop, 'config'))
    # 异步事件回路永久运行
    loop.run_forever()
