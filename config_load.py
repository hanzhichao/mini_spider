#!/usr/bin/env python
"""
load config file
default config file: ./conf/spider.conf
default section: 'spider'
"""
# -*- coding: utf-8 -*-
import platform

# handle the differences between python2 and python3
if (platform.python_version()) < '3':
    import ConfigParser
    import codecs
else:
    from configparser import ConfigParser
    from configparser import RawConfigParser
    from configparser import NoOptionError
    from configparser import NoSectionError


class Config(Object):
    """
    Customized Config Class, to get option from config files
    """
    def __init__(self, config_file_path):
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

    def get(self, option, section='spider'):
        """ get option from the config file"""
        return self.cf.get(section, option)
