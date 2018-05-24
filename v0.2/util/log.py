# env/usr/bin python 
# -*- coding: utf-8 -*-

"""

"""
import os
import sys
import time
import logging
sys.path.append("..")
from util.config import project_dir


class Log(object):
    _instance = None

    def __new__(cls):
        return cls._instance if cls._instance else super(Log, cls).__new__(cls)

    def __init__(self):
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        log_file = os.path.join(project_dir, 'log', today + '.log')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(log_file, mode='a')
        ch = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - \
            %(lineno)d - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    log = Log()
    logger = log.get_logger()
    logger.debug("hello")