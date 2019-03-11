#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@name: start.py
@editor: PyCharm
@Date: 2019/1/16 14:10
@Author: ly
@Description: 服务启动脚本
"""
import os
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options
from tornado.ioloop import IOLoop
from handlers.riqian import Riqian

define('port', default=80, type=int, help='监听端口...')

ROOT = os.path.dirname(__file__)
STATIC_PATH = os.path.join(ROOT, 'static')

URL_ROUTE = [
    (r'/riqian', Riqian),
    (r'/(.*)', StaticFileHandler, {'path': STATIC_PATH, 'default_filename': 'index.html'}),
]

SETTINGS = {
    'debug': True,
    'cookie_secret': 'Tpmlb5C2SQ6BFnDW124cz9ca1ZSxt0G6sUaisseby0g='
}

if __name__ == '__main__':
    options.parse_command_line()
    app = Application(handlers=URL_ROUTE, **SETTINGS)
    try:
        app.listen(options.port)
        print('************************************************')
        print('服务启动，监听端口{}。'.format(options.port))
        print('************************************************')
        IOLoop.current().start()
    except KeyboardInterrupt as e:
        print('************************************************')
        print('停止服务...')
        IOLoop.current().stop()
        print('服务停止！')
        print('************************************************')
    except Exception as e:
        print('************************************************')
        print('服务启动失败，原因：{}。'.format(e.args[0]))
        print('************************************************')
