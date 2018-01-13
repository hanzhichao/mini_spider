#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import json
import subprocess


class TestOptionParser(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    @staticmethod
    def cmd(cmd):
        mytask = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
    
        stdstr = mytask.stdout.read()
        return stdstr
    
    def test_option_help(self):
        self.assertTrue('show this help message and exit' in self.cmd('python ../mini_spider.py -h'))
        self.assertTrue('show this help message and exit' in self.cmd('python ../mini_spider.py --help'))
    
    def test_option_version(self):
        project_info_file = os.path.join(os.path.dirname(__file__), "../.project_info.json")
        with open(project_info_file, "r") as f:
            version = json.load(f)['version']
        self.assertTrue(version in self.cmd('python ../mini_spider.py -v'))
        self.assertTrue(version in self.cmd('python ../mini_spider.py --version'))
    
    def test_option_conf(self):
        pass
    
    def test_option_conf_no_args(self):
        self.assertTrue('option requires 1 argument' in self.cmd('python ../mini_spider.py -c'))
        self.assertTrue('option requires 1 argument' in self.cmd('python ../mini_spider.py --conf'))
        
    def test_config_file_not_exist(self):
        pass
