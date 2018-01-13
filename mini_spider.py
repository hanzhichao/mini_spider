#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import os
import log
import seedfile_load
import option_parser
import config_load
import crawl_thread


def main():
    """
    main method
    :return: None
    """
    # handle command options
    if option_parser.options.conf:
        config = config_load.Config(option_parser.options.conf)
    else:
        config = config_load.Config()
    
    if option_parser.options.version:
        project_info_file = os.path.join(os.path.dirname(__file__), ".project_info.json")
        with open(project_info_file, "r") as f:
            print(json.load(f)['version'])
        exit()

    # get config options
    reg = config.get('target_url')
    max_depth = int(config.get('max_depth'))
    crawl_interval = float(config.get('crawl_interval'))
    crawl_timeout = float(config.get('crawl_timeout'))
    
    # logging start time
    log.logger.debug("spider start at: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " ---")
    start_time = time.time()

    # iterate base_urls from seed file
    for base_url in seedfile_load.get_urls(seed_file=config.get('url_list_file')):
        
        # make dirs in output_dir for each url
        output_dir = os.path.join(config.get('output_directory'), *base_url.split('/')[2:])
        log.logger.debug("output_dir: " + output_dir)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except IOError:
                log.logger.error("make out_put dir error")
                
        crawl_thread.url_queue.put(base_url)   # add base_url to the url_queue of crawl_thread moudle
        log.logger.debug("base url: %s" % base_url)
        log.logger.debug("max depth: " + str(max_depth))
        
        # BFs-breadth first, consume all urls of url_queue,put new producing urls to sub_url_queue
        # and then redirect sub_url_queue to url_queue
        for current_depth in range(0, max_depth):
            log.logger.debug("current depth: %s" % current_depth)
            log.logger.debug("current queue size: %d" % crawl_thread.url_queue.qsize())
            crawl_thread.muti_crawl(thread_count=int(config.get('thread_count')),
                                    reg=reg,
                                    crawl_interval=crawl_interval,
                                    crawl_timeout=crawl_timeout,
                                    output_dir=output_dir)
            
            # make sub_url_queue the working queue
            crawl_thread.url_queue = crawl_thread.sub_url_queue
            current_depth += 1
    
    # logging end time and full duration
    log.logger.debug("spider gracefully end at: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) +
                     " Full Duration: " + str(time.time() - start_time) + 's' + " ---")


main()
