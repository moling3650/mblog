#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-06 14:35:53
# @Author  : moling (365024424@qq.com)
# @Link    : #
# @Version : 0.1
import re
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import HtmlFormatter
from .markdown2 import markdown
from .errors import APIPermissionError, APIValueError


# 网页翻页信息类
class Page(object):

    '''
    Page object for display pages.
    '''

    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index > self.page_count):
            self.offset = 0
            self.limit = 0
            self.page_index = self.page_count
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1


# 获取合法的页面引索
def set_valid_value(num_str, value=1):
    try:
        return max(int(num_str), 1)
    except ValueError:
        return value


def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


def check_string(**kw):
    for field, string in kw.items():
        if not string or not string.strip():
            raise APIValueError(field, '%s cannot be empty.' % field)


def markdown_highlight(content):
    return re.sub(
        r'<pre><code>(?P<code>.+?)</code></pre>',
        lambda m: highlight(m.group('code'), Python3Lexer(), HtmlFormatter()),
        markdown(content), flags=re.S)
