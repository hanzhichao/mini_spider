#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import webpage_parser


class TestSeedFileLoad(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_save_html(self):
        webpage_parser.save('pycm.baidu.com:8081/page1.html', './output')
        try:
            with open('../output/baidu.html', 'r') as f:
                html = f.read()
            self.assertTrue('page1.html' in html)
        except IOError:
            self.fail('no html fail saved')

    def test_save_html_with_dirs(self):
        webpage_parser.save('pycm.baidu.com:8081/page1/page1_1.html', 'output')
        try:
            with open('../output/page1/page1_1.html', 'r') as f:
                html = f.read()
            self.assertTrue('page1_1' in html)
        except IOError:
            self.fail('no html fail saved')

