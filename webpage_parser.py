#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import platform
import HTMLParser
import log
# handle the difference between python2 and python3
if (platform.python_version()) < '3':
    import urllib
else:
    import urllib.request as urllib


class UrlParser(HTMLParser.HTMLParser):
    def __init__(self):
        self.links = []
        HTMLParser.HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.links.append(value)
    
    def get_links(self):
        return self.links


def retrieve_urls(current_url, pattern):
    """
    retrieve urls from url using regex pattern
    @:param url type:str should contains 'http://'
    @:param reg type:str regex pattern read from spider.conf
    :return url_list(type:list) if current_url is valid
    :return None if url is invalid
    """
    parser = UrlParser()

    try:
        parser.feed(urllib.urlopen(current_url).read())
        links = parser.get_links()
        # log.logger.debug("links: " + ','.join(links))
        reg_pattern = re.compile(pattern)
        # log.logger.debug('reg pattern: ' + pattern)
        url_list = []
        for link in links:
            # log.logger.debug('link: ' + link)
            match = re.match(reg_pattern, link)
            
            if match:
                # log.logger.debug('match result: ' + match.group())
                url_list.append(match.group())
            else:
                pass
                # log.logger.debug('match result: ' + "None")
            
        url_list = list(set(url_list))  # remove duplicated urls
        # log.logger.debug("url_list: " + ",".join(url_list))
        
        # if urls in url_list not contains 'http' then add current_url before
        # if urls contains 'javascript' add current_url and the last part
        def format_url(url):
            if "&quot;" in url:
                url = url.replace("&quot;", '"')
            if "&nbsp;" in url:
                url = url.replace("&nbsp;", " ")
                
            if 'http' in url:
                return url
            elif url[:2] == '//':
                return 'http:' + url
            else:
                base_url = '/'.join(current_url.split('/')[:-1])
                if 'javascript' in url:
                    if '=' in url:
                        try:
                            return base_url + '/' + url.split('=')[1][1:]
                        except IndexError:
                            log.logger.warning("url: %s format fail" % url)
                    else:
                        return None
                else:
                    return base_url + '/' + url

        url_list = map(format_url, url_list)
        
        return url_list
    except IOError:
        log.logger.warning("current url: %s is invalid" % current_url)
        return None


def save_page(url, output_dir):
    """
    save url html page to output_dir
    :param url: url to save, should contains .html, will makedirs if uri contains muti dirs
    :param output_dir: base output dir
    :return: None
    """
    if output_dir[0] != '/':
        if output_dir[:2] == './':
            output_dir = output_dir[2:]
        output_dir = os.path.join(os.path.dirname(__file__).decode("utf-8"), output_dir)
    log.logger.debug("url: " + url)
    uri = url.split('/')[3:]
    log.logger.debug("uri: " + ','.join(uri))
    if uri:
        file_dir = os.path.join(output_dir, *uri[:-1])  # eg. ./output/page1/page1_1
        file_name = uri[-1]
    else:
        file_dir = output_dir
        file_name = 'index.html'
    
    log.logger.debug("file_dir: " + file_dir)
    if not os.path.exists(file_dir):
        if 'Windows' in platform.platform():
            try:
                os.makedirs(file_dir)  # make sub dirs in output dir
            except WindowsError:
                log.logger.error("create dirs: %s fail", file_dir)
        else:
            try:
                os.makedirs(file_dir)  # make sub dirs in output dir
            except OSError:
                log.logger.error("create dirs: %s fail", file_dir)
            
    file_path = os.path.join(file_dir, file_name)  # eg. page1_1_1.html
    log.logger.debug("file_path: " + file_path)
    try:
        urllib.urlretrieve(url, file_path)  # save html
    except IOError:
        log.logger.error("save file: %s fail" % file_path)
