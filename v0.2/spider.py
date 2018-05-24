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
from util.link_producer import LinkProducer
from util.link_consumer import LinkConsumer


cf = Config()
log = Log()
logger = log.get_logger()

max_depth = cf.get('max_depth')
def main():
    try:
        with open("urls.txt") as f:
            seeds = map(lambda x:x.strip(), f.readlines())
    except IOError:
        logger.error("Open file: 'urls.txt' fail")

    task_queue = Queue.Queue()
    data_queue = Queue.Queue()
    for url in seeds:
        task_queue.put(url)

    cur_depth = 0
    crawl_timeout = float(cf.get('crawl_timeout'))

    thread_count = int(cf.get('thread_count'))
    producers = []
    consumers = []
    for i in range(0, thread_count):
        producer = LinkProducer('Producer', task_queue, data_queue)
        consumer = LinkConsumer('Consumer', data_queue)
        producers.append(producer)
        consumers.append(consumer)

    for i in range(0, thread_count):
        producers[i].start()
        consumers[i].start()
    
    for i in range(0, thread_count):
        producers[i].join(crawl_timeout)
        consumers[i].join(crawl_timeout)


if __name__ == '__main__':
    main()