#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform

# handle the differences between python2 and python3
if (platform.python_version()) < '3':
    import ConfigParser
    import codecs
else:
    from configparser import ConfigParser, RawConfigParser, NoOptionError, NoSectionError

DEFAULT_CONF = os.path.join(os.path.dirname(__file__), 'conf/spider.conf')
DEFAULT_SECTION = 'spider'


class Config:
    def __init__(self, config_file_path=DEFAULT_CONF):
        try:
            if (platform.python_version()) < '3':
                # python 2
                self.cf = ConfigParser.ConfigParser()
                with codecs.open(config_file_path, encoding='utf-8-sig') as f:
                    self.cf.readfp(f)
            else:
                # python3
                # self.cf = RawConfigParser()
                # self.cf.read(config_file_path, encoding='utf8')
                self.cf = ConfigParser()
                self.cf.read(config_file_path)
        except IOError:
            raise IOError

    def get(self, option, section=DEFAULT_SECTION):
        """ get option from the config file"""
        return self.cf.get(section, option)
