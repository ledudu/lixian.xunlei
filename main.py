#/usr/bin/env python
# -*- encoding: utf8 -*-
# author: binux<17175297.hk@gmail.com>

import os
import tornado
import logging
from time import time
from tornado import web
from tornado.ioloop import IOLoop
from tornado.options import define, options

define("debug", default=True, help="debug mode")
define("port", default=8880, help="the port tornado listen to")
define("username", help="xunlei vip login name")
define("password", help="xunlei vip password")
define("check_interval", default=60*60, help="the interval of checking login status")
define("cross_userscript", default="http://userscripts.org/scripts/show/117745",
        help="the web url of cross cookie userscirpt")
define("cross_userscript_local", default="/static/cross-cookie.userscript",
        help="the local path of cross cookie userscirpt")
define("cross_cookie_url", default="http://lixian.vip.xunlei.com/help.html",
        help="the url to insert to")
define("cookie_str", default="gdriveid=%s; domain=.vip.xunlei.com",
        help="the cookie insert to cross path")

class Application(web.Application):
    def __init__(self):
        from handlers import handlers, ui_modules
        from libs.util import ui_methods
        from libs.task_manager import TaskManager
        settings = dict(
            debug=options.debug,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),

            ui_modules=ui_modules,
            ui_methods=ui_methods,
        )
        super(Application, self).__init__(handlers, **settings)

        self.task_manager = TaskManager(
                    username = options.username,
                    password = options.password,
                    check_interval = options.check_interval,
                )
        if not self.task_manager.islogin:
            raise Exception, "xunlei login error"
        logging.info("load finished!")

def main():
    tornado.options.parse_command_line()

    application = Application()
    application.listen(options.port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()
