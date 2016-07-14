#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 19:09:28
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1

import asyncio
import logging

from app.frame.orm import create_pool
from app.models import User
from config.orm_test import db_config

async def test():
    await create_pool(loop, **db_config)

    # 测试count rows语句
    rows = await User.countRows()
    logging.info('rows is: %s' % rows)

    # 测试insert into语句
    if rows < 2:
        for idx in range(5):
            u = User(
                name='test%s' % (idx),
                email='test%s@orm.org' % (idx),
                password='pw',
                image='/static/img/user.png'
            )
            rows = await User.countRows(where='email = ?', args=[u.email])
            if rows == 0:
                await u.save()
            else:
                print('the email was already registered...')

    # 测试select语句
    users = await User.findAll(orderBy='created_at')
    for user in users:
        logging.info('name: %s, password: %s' % (user.name, user.password))

    # 测试update语句
    user = users[1]
    user.email = 'guest@orm.com'
    user.name = 'guest'
    await user.update()

    # 测试查找指定用户
    test_user = await User.find(user.id)
    logging.info('name: %s, email: %s' % (test_user.name, test_user.email))

    # 测试delete语句
    users = await User.findAll(orderBy='created_at', limit=(1, 2))
    for user in users:
        logging.info('delete user: %s' % (user.name))
        await user.remove()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
