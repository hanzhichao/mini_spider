# env/usr/bin python 
# -*- coding: utf-8 -*-

"""
1. 解析网页，提取links
2. 匹配需要抓取的url,生产待
"""
import re
import sys
import time
import Queue
import urllib
import threading
import HTMLParser
sys.path.append("..")
from util.log import Log
from util.config import Config

reload(sys)
sys.setdefaultencoding('utf-8') 

cf = Config()
log = Log()
logger = log.get_logger()
visited_list = []

class LinkParser(HTMLParser.HTMLParser):
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


class LinkProducer(threading.Thread):
    def __init__(self, name, task_queue, data_queue):
        threading.Thread.__init__(self, name=name)
        self.task_queue = task_queue
        self.sub_task_queue = Queue.Queue()
        self.data_queue = data_queue
        self.link_parser = LinkParser()

    def run(self):
        while not self.task_queue.empty():
            cur_url = self.task_queue.get()
            if not cur_url in visited_list:
                sub_links = self._parse_links(cur_url)
                for link in sub_links:
                    self.data_queue.put(link)
                    self.sub_task_queue.put(link)
                time.sleep(float(cf.get('crawl_timeout')))

    def get_sub_task_queue(self):
        return self.sub_task_queue
           
    def _parse_links(self, cur_url):
        visited_list.append(cur_url)
        try:
            html = urllib.urlopen(cur_url).read()
            self.link_parser.feed(self.link_parser.unescape(html))
        except IOError:
            log.logger.error("Current url: %s open error" % cur_url)
            return None

        all_links = self.link_parser.get_links()
        reg_pattern = re.compile(cf.get('target_url'))
        target_links = list(filter(lambda link:re.match(reg_pattern, link), all_links))
        return self._formats_links(cur_url, list(set(target_links)))

    def _formats_links(self, cur_url, links):
        http_or_https = cur_url.split(":")[0]
        if len(cur_url.split('/')) > 3:
            pre_url = "/".join(cur_url.split('/')[:-1])
        else:
            pre_url = cur_url

        def _format(link):
            if link.endswith('/'):
                link = link[:-1]
            if 'javascript' in link:
                return None
            elif http_or_https in link:
                return link
            elif link.startswith("//"):
                return http_or_https + ":" + link
            else:
                return "/".join((pre_url, link))

        return list(set(map(_format, links)))





if __name__ == '__main__':
    main()