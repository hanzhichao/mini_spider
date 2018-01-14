#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import webpage_parser


class TestSeedFileLoad(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    @staticmethod
    def format_url(current_url, url):
        if "&quot;" in url:
            url = url.replace("&quot;", '"')
        if "&nbsp;" in url:
            url = url.replace("&nbsp;", " ")
    
        if 'http' in url:
            return url
        elif url[:2] == '//':
            return 'http:' + url
        elif 'javascript' in url:
            if '=' in url:
                try:
                    return current_url + '/' + url.split('=')[1][1:]
                except IndexError:
                    print("url: %s format fail" % url)
            else:
                return None
        else:
            return current_url + '/' + url
    
    def test_save_html(self):
        webpage_parser.save_page('pycm.baidu.com:8081/page1.html', './output')
        try:
            with open('../output/baidu.html', 'r') as f:
                html = f.read()
            self.assertTrue('page1.html' in html)
        except IOError:
            self.fail('no html fail saved')

    def test_save_html_with_dirs(self):
        webpage_parser.save_page('pycm.baidu.com:8081/page1/page1_1.html', 'output')
        try:
            with open('../output/page1/page1_1.html', 'r') as f:
                html = f.read()
            self.assertTrue('page1_1' in html)
        except IOError:
            self.fail('no html fail saved')

    def test_format_url(self):
        self.assertEqual(self.format_url('http://www.baidu.com', '//www.baidu.com/cache/sethelp/help.html'),
                         'http://www.baidu.com/cache/sethelp/help.html')
        self.assertEqual(self.format_url('http://www.baidu.com', 'http://www.baidu.com/cache/sethelp/help.html'),
                         'http://www.baidu.com/cache/sethelp/help.html')
        self.assertEqual(self.format_url('http://www.baidu.com', 'https://www.baidu.com'),
                         'https://www.baidu.com')
        self.assertEqual(self.format_url('http://www.baidu.com', 'javascript;'),
                         None)
        self.assertEqual(self.format_url('http://www.baidu.com', 'javascript:location.href=&quot;page4.html'),
                         'http://www.baidu.com/page4.html')
        self.assertEqual(self.format_url('http://www.baidu.com', 'page4.html'),
                         'http://www.baidu.com/page4.html')
        