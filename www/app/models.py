#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 18:47:39
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1

import functools
import hashlib
import time
import uuid

from app import COOKIE_KEY, COOKIE_NAME
from app.frame.fields import *
from app.frame.orm import Model

StringField = functools.partial(StringField, ddl='varchar(50)')


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


# 定义用户类
class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id)
    email = StringField()
    password = StringField()
    admin = BooleanField()
    name = StringField()
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

    async def save(self):
        self.id = next_id()
        sha1_pw = '%s:%s' % (self.id, self.password)
        self.password = hashlib.sha1(sha1_pw.encode('utf-8')).hexdigest()
        await super().save()

    def signin(self, response, max_age=86400):
        expires = str(int(time.time() + max_age))
        s = '%s-%s-%s-%s' % (self.id, self.password, expires, COOKIE_KEY)
        L = [self.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
        response.set_cookie(COOKIE_NAME, '-'.join(L), max_age=max_age, httponly=True)
        return response

    @classmethod
    def signout(cls, response):
        response.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
        return response

    @classmethod
    async def find_by_cookie(cls, cookie_str):
        if not cookie_str:
            return None
        try:
            L = cookie_str.split('-')
            if len(L) != 3:
                return None
            uid, expires, sha1 = L
            if int(expires) < time.time():
                return None
            user = await cls.find(uid)
            if user is None:
                return None
            s = '%s-%s-%s-%s' % (uid, user.password, expires, COOKIE_KEY)
            if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
                logging.info('invalid sha1')
                return None
            user.password = '******'
            return user
        except Exception as e:
            logging.exception(e)
            return None


# 定义博客类
class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id)
    user_id = StringField()
    user_name = StringField()
    user_image = StringField(ddl='varchar(500)')
    name = StringField()
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


# 定义评论类
class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id)
    blog_id = StringField()
    user_id = StringField()
    user_name = StringField()
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Oauth(Model):
    __table__ = 'oauth'

    id = StringField(primary_key=True)
    user_id = StringField()
    created_at = FloatField(default=time.time)
