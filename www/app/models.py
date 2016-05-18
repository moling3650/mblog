#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-05 18:47:39
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1

import functools, hashlib, time, uuid

from app import COOKIE_KEY
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

    async def register(self):
        self.id = next_id()
        sha1_pw = '%s:%s' % (self.id, self.password)
        self.password = hashlib.sha1(sha1_pw.encode('utf-8')).hexdigest()
        await self.save()

    def generate_cookie(self, max_age):
        expires = str(int(time.time() + max_age))
        s = '%s-%s-%s-%s' % (self.id, self.password, expires, COOKIE_KEY)
        L = [self.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
        return '-'.join(L)

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
            user.passwd = '******'
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