#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-05 09:33:01
# @Author  : moling (365024424@qq.com)
# @Link    : http://qiangtaoli.com
# @Version : $Id$
import time
import mistune
from datetime import datetime
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


class HighlightRenderer(mistune.Renderer):

    def block_code(self, code, lang):
        guess = 'python3'
        if code.lstrip().startswith('<?php'):
            guess = 'php'
        elif code.lstrip().startswith(('<', '{%')):
            guess = 'html+jinja'
        elif code.lstrip().startswith(('function', 'var', '$')):
            guess = 'javascript'

        lexer = get_lexer_by_name(lang or guess, stripall=True)
        return highlight(code, lexer, HtmlFormatter())

# 因为页面经常用md渲染，所以定义为常量，不用在函数内重复申请释放内存
markdown = mistune.Markdown(renderer=HighlightRenderer(), hard_wrap=True)


def marked_filter(content):
    return markdown(content) if isinstance(content, (str, bytes)) else ''
