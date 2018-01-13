#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import platform
import log
# handle the difference between python2 and python3
if (platform.python_version()) < '3':
    import urllib
else:
    import urllib.request as urllib


def retrieve_urls(current_url, reg):
    """
    retrieve urls from url using regex pattern
    @:param url type:str should contains 'http://'
    @:param reg type:str regex pattern read from spider.conf
    :return url_list(type:list) if current_url is valid
    :return None if url is invalid
    """
    try:
        html = urllib.urlopen(current_url).read()
        reg = re.compile(reg)
        url_list = re.findall(reg, html)
        url_list = list(set(url_list))  # remove duplicated urls
        
        # if urls in url_list not contains 'http' then add current_url before
        # if urls contains 'javascript' add current_url and the last part
        url_list = map(lambda x: x if 'http' in x \
            else (current_url + '/' + x if 'javascript' not in x \
                else current_url + '/' + x.split('=')[1].split(';')[1]), url_list)
        
        return url_list
    except IOError:
        log.logger.warning("current url: %s is invalid" % current_url)
        return None


def save(url, output_dir):
    """
    save url html page to output_dir
    :param url: url to save, should contains .html, will makedirs if uri contains muti dirs
    :param output_dir: base output dir
    :return: None
    """
    log.logger.debug("url: " + url)
    uri = url.split('/')[3:]
    log.logger.debug(uri)
    if uri:
        file_dir = os.path.join(output_dir, *uri[:-1])  # eg. ./output/page1/page1_1
        file_name = uri[-1]
    else:
        file_dir = output_dir
        file_name = 'index.html'
    
    log.logger.debug("file_dir: " + file_dir)
    if not os.path.exists(file_dir):
        try:
            os.makedirs(file_dir)  # make sub dirs in output dir
        except IOError:
            log.logger.error("create dirs fail")
    file_path = os.path.join(file_dir, file_name)  # eg. page1_1_1.html
    log.logger.debug("file_path: " + file_path)
    try:
        urllib.urlretrieve(url, file_path)  # save html
    except IOError:
        log.logger.error("save file: %s fail" % file_path)
