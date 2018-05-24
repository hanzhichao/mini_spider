# env/usr/bin python 
# -*- coding: utf-8 -*-

"""

"""
import os
import sys
import time
import Queue
import urllib
import threading
sys.path.append("..")
from util.log import Log
from util.config import Config
from util.config import project_dir

cf = Config()
log = Log()
logger = log.get_logger()


class LinkConsumer(threading.Thread):
    def __init__(self, name, data_queue):
        threading.Thread.__init__(self, name=name)
        self.data_queue = data_queue

    def run(self):
        while not self.data_queue.empty():
            link = self.data_queue.get()
            self._save(link)


    def _save(self, link):
        output_dir = os.path.join(project_dir, cf.get('output_directory')).strip()
        cur_url_split = cur_url.split('/')
        if len(cur_url_split) > 3:
            output_dir = os.path.join(cur_url_split[:-1]).strip()
            file_name = cur_url_split[-1]
        else:
            file_name = 'index.html'

        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError:
                log.logger.error("Create output dir: %s fail", out_put_dir)
        try:
            urllib.urlretrieve(file_name, output_dir)  # save html
        except IOError:
            log.logger.error("Save file: %s into dir: %s fail" % (file_name, output_dir))
