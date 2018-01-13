#!/usr/bin/env python
# -*- coding: utf-8 -*-
import platform
import time
from threading import Thread, Lock
import webpage_parser
import log
# handle the differences between python2 and python3
if (platform.python_version()) < '3':
    import Queue
else:
    import queue as Queue

# store the urls which had been crawled and saved
visited_url_list = []
url_queue = Queue.Queue(maxsize=-1)
sub_url_queue = Queue.Queue(maxsize=-1)
visited_url_list_lock = Lock()  # lock the visited_url_list while appending new url


def muti_crawl(thread_count, reg, crawl_interval, crawl_timeout, output_dir):
    """
    run multiple threads to run crawl(reg, output_dir)
    :param thread_count: type:int thread number read from config file
    :param reg: regex pattern for retrieving urls
    :param crawl_interval: threads waiting time
    :param crawl_timeout: threads timeout time
    :param output_dir: html page output dictionary
    :return: None
    """
    
    # new thread list
    threads = []
    
    # create threads
    for i in range(thread_count):
        t = Thread(target=crawl, args=(reg, output_dir))
        threads.append(t)
    
    # start threads
    for i in range(thread_count):
        threads[i].setDaemon(True)
        threads[i].start()
        time.sleep(crawl_interval)  # waiting time
    
    # waiting all threads to complete
    for i in range(thread_count):
        threads[i].join(crawl_timeout)


def crawl(reg, output_dir):
    """
    get url form the working queue, retrieve new urls and put to another queue then save the html page to output_dir
    :param reg: type:str retrieve url regex pattern
    :param output_dir: type:str read from config file
    :return: None
    """
    while not url_queue.empty():
        # get one url from url_queue
        current_url = url_queue.get()
        
        # retrieve urls from current_url using reg as regex pattern
        urls = webpage_parser.retrieve_urls(current_url, reg)
        
        # save current_url as html page in output_dir
        webpage_parser.save(current_url, output_dir)
        
        # lock the visited_url_list while appending new url
        visited_url_list_lock.acquire()
        visited_url_list.append(current_url)
        visited_url_list_lock.release()
        
        # if current_url is valid and has urls
        if urls:
            log.logger.debug("current url: %s" % current_url)
            for url in urls:
                if url not in visited_url_list:
                    # put new urls to new queue if url is not visited
                    sub_url_queue.put(url)
        
        

