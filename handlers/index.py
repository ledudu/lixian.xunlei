# -*- encoding: utf-8 -*-
# author: binux<17175297.hk@gmail.com>

import logging
import json
from tornado.web import HTTPError
from tornado.options import options
from .base import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        tasks = self.xunlei.get_task_list()
        self.render("index.html", tasks=tasks)

class GetLiXianURL(BaseHandler):
    def get(self):
        task_id = int(self.get_argument("task_id"))
        task = self.xunlei.get_task(task_id)
        files = self.xunlei.get_file_list(task_id)

        if task is None:
            raise HTTPError(404)
        if files is None:
            raise HTTPError(500)

        cookie = options.cookie_str % self.xunlei.gdriveid
        self.render("lixian.html", task=task, files=files, cookie=cookie)

class AddTaskHandler(BaseHandler):
    def post(self):
        url = self.get_argument("url")
        
        result = self.xunlei.add_task(url)
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps({"result": result}))

handlers = [
        (r"/", IndexHandler),
        (r"/get_lixian_url", GetLiXianURL),
        (r"/add_task", AddTaskHandler),
        ]
ui_modules = {}
