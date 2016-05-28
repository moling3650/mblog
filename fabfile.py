#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-18 14:43:49
# @Author  : moling (365024424@qq.com)
# @Link    : #
import os
from datetime import datetime
from fabric.api import *

_REMOTE_BASE_DIR = '/home/ubuntu/mblog'
_TAR_FILE = 'dist-mblog.tar.gz'
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE

env.hosts = ['119.29.191.109']
env.user = 'ubuntu'
env.password = '******'
env.key_filename = 'D:\\tk'


def _now():
    return datetime.now().strftime('%y-%m-%d_%H:%M:%S')


def build():
    includes = ['app', 'config', '*.py']
    excludes = ['__pycache__', '*.pyc', '*.pyo', 'orm_test.*']
    local('rm -f dist/%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))


def deploy():
    newdir = 'www-%s' % _now()
    sudo('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' % newdir)
    with settings(warn_only=True):
        sudo('supervisorctl restart mblog')
        sudo('service nginx restart')


def go():
    build()
    deploy()
