#!/usr/bin/env python
""" retrieve urls from page and save page to output directory"""
# -*- coding: utf-8 -*-
import re
import os
import platform
import log
import urllib
import HTMLParser
import sys
import log

reload(sys)
sys.setdefaultencoding('utf-8') 

class UrlParser(HTMLParser.HTMLParser):
    """Costomized url parser class, subclass of HTMLParser.HTMLParser"""
    def __init__(self):
        """ self.links use to return """
        self.links = []
        HTMLParser.HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attrs):
        """ get all node start tag is <a>"""
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.links.append(value)
    
    def get_links(self):
        """return all links"""
        return self.links


def _format_url(current_url, url):
    """ 
    format url if is not complete or contains special characters,
    if urls in url_list not contains 'http' then add current_url before,
    if urls contains 'javascript' add current_url and the last part

    :@param url: <type: str> url retrieve from html links
    """
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


def retrieve_urls(current_url, pattern):
    """
    retrieve urls from url using regex pattern
    @:param url: <type:str> should contains 'http://'
    @:param reg: <type:str> regex pattern read from spider.conf
    :return url_list: <type:list> if current_url is valid
    :return None if url is invalid
    """
    parser = UrlParser()

    try:
        parser.feed(urllib.urlopen(current_url).read())
    except IOError:
        log.logger.warning("current url: %s is invalid" % current_url)
        return None

    links = parser.get_links()
    reg_pattern = re.compile(pattern)

    url_list = []
    for link in links:
        match = re.match(reg_pattern, link)   
        if match:
            url_list.append(match.group())
     
    # format urls
    formated_urls = []
    for url in list(set(url_list)):
        formated_urls.append(_format_url(current_url, url))
    return formated_urls
    


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
        output_dir = os.path.join(os.path.dirname(__file__), output_dir)
    # log.logger.debug("url: " + url)
    uri = url.split('/')[3:]
    # log.logger.debug("uri: " + ','.join(uri))
    if uri:
        file_dir = os.path.join(output_dir, *uri[:-1])  # eg. ./output/page1/page1_1
        file_name = uri[-1]
    else:
        file_dir = output_dir
        file_name = 'index.html'
    
    # log.logger.debug("file_dir: " + file_dir)
    file_dir = file_dir.strip()
    if not os.path.exists(file_dir):
        try:
            # log.logger.debug("create file_dir: " + file_dir)
            os.makedirs(file_dir)  # make sub dirs in output dir
        except OSError:
            log.logger.error("create dirs: %s fail", file_dir)
            
    file_path = os.path.join(file_dir, file_name)  # eg. page1_1_1.html
    
    try:
        log.logger.debug("save file: " + file_path)
        urllib.urlretrieve(url, file_path)  # save html
    except IOError:
        log.logger.error("save file: %s fail" % file_path)
