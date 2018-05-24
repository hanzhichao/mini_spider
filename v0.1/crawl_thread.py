#!/usr/bin/env python
"""
multiple threads crawl the given urls using given regex pattern
"""
# -*- coding: utf-8 -*-
import platform
import time
import json
import Queue
from threading import Thread
from threading import Lock
import webpage_parser
import log


# store the urls which had been crawled and saved
visited_url_list = []
url_queue = Queue.Queue()
sub_url_queue = Queue.Queue()
visited_url_list_lock = Lock()  # lock the visited_url_list while appending new url
save_page_lock = Lock()


def muti_crawl(thread_count, reg, crawl_interval, crawl_timeout, output_dir):
    """
    run multiple threads to run crawl(reg, output_dir)
    :param thread_count: <type:int> thread number read from config file
    :param reg: <type:str> regex pattern for retrieving urls
    :param crawl_interval: <type:str> threads waiting time
    :param crawl_timeout: <type:str> threads timeout time
    :param output_dir: <type:str> html page output dictionary
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
    :param reg: <type:str> retrieve url regex pattern
    :param output_dir: <type:str> read from config file
    :return: None
    """
    
    # get one url from url_queue
    
    current_url = url_queue.get()
    
    # retrieve urls from current_url using reg as regex pattern
    urls = webpage_parser.retrieve_urls(current_url, reg)
    
    # save current_url as html page in output_dir
    save_page_lock.acquire()
    webpage_parser.save_page(current_url, output_dir)
    save_page_lock.release()
    
    # lock the visited_url_list while appending new url
    visited_url_list_lock.acquire()
    visited_url_list.append(current_url)
    visited_url_list_lock.release()
    
    # if current_url is valid and has urls
    if urls:
        # log.logger.debug("current url: %s" % current_url)
        # log.logger.debug("urls in current url page: %s" % json.dumps(urls))
        for url in set(urls):
            if not url in visited_url_list:
                # put new urls to new queue if url is not visited
                sub_url_queue.put(url)

