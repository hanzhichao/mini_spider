#!/usr/bin/env python
""" test option_parser.py using unittest """
# -*- coding: utf-8 -*-
import os
import unittest
import json
import subprocess


class TestOptionParser(unittest.TestCase):
    """subclass of unittest.TestCase """
    
    @staticmethod
    def cmd(cmd):
        """ execute System command and return stdout or stderr"""
        mytask = subprocess.Popen(cmd,
                                  shell=True,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
    
        stdstr = mytask.stdout.read()
        return stdstr
    
    def test_option_help(self):
        """ test option -h and --help """
        result = self.cmd('python ../mini_spider.py -h')
        self.assertTrue('show this help message and exit' in result)
        
        result = self.cmd('python ../mini_spider.py --help')
        self.assertTrue('show this help message and exit' in result)
    
    def test_option_version(self):
        """ test option -v and --version """
        project_info_file = os.path.join(os.path.dirname(__file__),
                                         "../.project_info.json")
        with open(project_info_file, "r") as f:
            version = json.load(f)['version']
        
        result = self.cmd('python ../mini_spider.py -v')
        self.assertTrue(version in result)
        
        result = self.cmd('python ../mini_spider.py --version')
        self.assertTrue(version in result)
    
    def test_option_conf_no_args(self):
        """ test option -c and --conf with no args """
        
        result = self.cmd('python ../mini_spider.py -c')
        self.assertTrue('option requires 1 argument' in result)
        
        result = self.cmd('python ../mini_spider.py --conf')
        self.assertTrue('option requires 1 argument' in result)
