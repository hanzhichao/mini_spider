# !/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import time
import os

DEFAULT_LOG_FILE_PRX = 'spider_'

log_dir = os.path.join(os.path.dirname(__file__),'log')

# def log_config(log_dir, output_log_lever, console_log_lever):
date = time.strftime('%Y%m%d', time.localtime(time.time()))
log_file = os.path.join(log_dir, DEFAULT_LOG_FILE_PRX + date + ".log")
logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_file, mode='a')
fh.setLevel(logging.DEBUG)   # output log_level

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)   # console log_level

formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
    
# return logger
