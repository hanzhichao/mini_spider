#!/usr/bin/env python
""" test seedfile_parser.py using unittest """
# -*- coding: utf-8 -*-
import unittest
import os
import seedfile_load


class TestSeedFileLoad(unittest.TestCase):
    """ subclass of unittest.TestCase """
    def setUp(self):
        """ read seed file and save the original content"""
        self.seed_file = os.path.join(os.path.dirname(__file__),
                                      '../seed/urls')
        self.origin_content = self.read_seed_file()
    
    def tearDown(self):
        """ write the original content to the seed file"""
        self.write_seed_file(self.origin_content)
    
    def read_seed_file(self):
        """ read seed file and return the content"""
        with open(self.seed_file) as f:
            return f.read()
        
    def write_seed_file(self, content):
        """ write content into seed file"""
        with open(self.seed_file, 'w') as f:
            f.write(content)
            
    def test_muti_lines(self):
        """ test seedfile contains multiple lines"""
        content = '''www.baiud.com
        www.sina.com
        www.sohu.com
        '''
        self.write_seed_file(content)
        urls = seedfile_load.get_urls(self.seed_file)
        self.assertTrue('www.baidu.com' in urls)
        self.assertTrue('www.sina.com' in urls)
        self.assertTrue('www.sohu.com' in urls)
