#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-06 14:35:53
# @Author  : moling (365024424@qq.com)
# @Link    : http://www.qiangtaoli.com
# @Version : 0.1
import re
from .errors import APIPermissionError, APIValueError

_RE_EMAIL = re.compile(r'^[a-zA-Z0-9\.\-\_]+\@[a-zA-Z0-9\-\_]+(\.[a-zA-Z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

# 网页翻页信息类
class Page(object):

    def __init__(self, item_count, index=1, size=10):
        self.last = item_count // size + (1 if item_count % size > 0 else 0)  # 尾页
        self.index = min(index, self.last) if item_count > 0 else 1           # 当前页
        self.offset = size * (index - 1)    # 数据库查询用，偏移N个元素
        self.limit = size                   # 一页有多少个元素


# 设置合法的查询字符串参数
def set_valid_value(num_str, value=1):
    try:
        num = int(num_str)
    except ValueError:
        return value
    return num if num > 0 else value


# 检查用户
def check_user(user, check_admin=True):
    if user is None:
        raise APIPermissionError('Please signin first.')
    elif check_admin and not user.admin:
        raise APIPermissionError('admin only')


# 检查字符串是否为空
def check_string(**kw):
    for field, string in kw.items():
        if not string or not string.strip():
            raise APIValueError(field, '%s cannot be empty.' % field)


# 检查邮箱和密码的格式是否合法
def check_email_and_password(email, password):
    if not email or not _RE_EMAIL.match(email):
        APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        APIValueError('password')
