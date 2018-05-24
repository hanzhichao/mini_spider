#!/usr/bin/env python
""" test webpage_parser using unittest"""
# -*- coding: utf-8 -*-
import unittest
import webpage_parser


class TestSeedFileLoad(unittest.TestCase):
    """ subclass of unittest.TestCase """

    @staticmethod
    def format_url(current_url, url):
        """ under testing method pick from webpage_parser.py """
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
        """ test save urls to output file"""
        webpage_parser.save_page('pycm.baidu.com:8081/page1.html', './output')
        try:
            with open('../output/baidu.html', 'r') as f:
                html = f.read()
            self.assertTrue('page1.html' in html)
        except IOError:
            self.fail('no html fail saved')

    def test_save_html_with_dirs(self):
        """ test mkdirs and save html pages"""
        webpage_parser.save_page('pycm.baidu.com:8081/page1/page1_1.html', 'output')
        try:
            with open('../output/page1/page1_1.html', 'r') as f:
                html = f.read()
            self.assertTrue('page1_1' in html)
        except IOError:
            self.fail('no html fail saved')

    def test_format_url(self):
        """ test format url method"""
        current_url = 'http://www.baidu.com'
        
        result = self.format_url(current_url, '//www.baidu.com/cache/sethelp/help.html')
        self.assertEqual(result, 'http://www.baidu.com/cache/sethelp/help.html')

        result = self.format_url(current_url, 'http://www.baidu.com/cache/sethelp/help.html')
        self.assertEqual(result, 'http://www.baidu.com/cache/sethelp/help.html')

        result = self.format_url(current_url, 'https://www.baidu.com')
        self.assertEqual(result, 'https://www.baidu.com')

        result = self.format_url(current_url, 'javascript;')
        self.assertEqual(result, None)

        result = self.format_url(current_url, 'javascript:location.href=&quot;page4.html')
        self.assertEqual(result, 'http://www.baidu.com/page4.html')

        result = self.format_url(current_url, 'page4.html')
        self.assertEqual(result, 'http://www.baidu.com/page4.html')
        
    def test_retrieve_urls(self):
        """ test retrieve_urls method """
        reg = '.*.html|htm'
        
        result = webpage_parser.retrieve_urls('http://www.baidu.com', reg)
        self.assertTrue('http://www.baidu.com/gaoji/preferences.html' in result)

        result = webpage_parser.retrieve_urls('http://www.baidu.com/gaoji/preferences.html', reg)
        self.assertTrue(result == [])

        result = webpage_parser.retrieve_urls('http://www.baidu.com/cache/sethelp/help.html', reg)
        self.assertTrue('http://www.baidu.com/duty/index.html' in result)

        result = webpage_parser.retrieve_urls('http://www.baidu.com/duty/index.html', reg)
        self.assertTrue('http://www.baidu.com/duty/yinsiquan.html' in result)
