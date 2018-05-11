#!/usr/bin/env python
"""
load config file
default config file: ./conf/spider.conf
default section: 'spider'
"""
# -*- coding: utf-8 -*-
import platform
import ConfigParser
import codecs


class Config(object):
    """
    Customized Config Class, to get option from config files
    """
    def __init__(self, config_file_path):
        """ init method when create new Config instance
        @:param config_file_path: <type:str> config file full path
        :return None
        :raise IOError: An error occurred when config file path is error or not exist.
        """
        try:
            self.cf = ConfigParser.ConfigParser()
            with codecs.open(config_file_path, encoding='utf-8-sig') as f:
                self.cf.readfp(f)
        except IOError:
            raise IOError

    def get(self, option, section='spider'):
        """
        get option from the config file
        @:param section: <type:str> section in the config file, eg. [spider], default section is 'spider' 
        @:param option: <type:str> option in the section eg. url_list_file
        :return <type:str> value of the option eg: ./seed/urls
        """
        return self.cf.get(section, option)
