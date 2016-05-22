#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 18:11:30
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1


class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<{0.__class__.__name__}, {0.column_type}: {0.name}>'.format(self)


class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntergerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        # String一般不作为主键，所以默认False, DDL是数据定义语言，为了配合mysql，所以默认设定为100的长度
        super().__init__(name, ddl, primary_key, default)


class TextField(Field):

    def __init__(self, name=None, default=None):
        # 这个是不能作为主键的对象，所以这里直接就设定成False了
        super().__init__(name, 'text', False, default)
