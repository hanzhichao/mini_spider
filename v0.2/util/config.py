# -*- coding: utf-8 -*-

"""

"""
import os
import codecs
import ConfigParser

project_dir = os.path.dirname(os.path.dirname(__file__))


class Config(object):

    def __init__(self, config_file='default.conf'):
        self.cf = ConfigParser.ConfigParser()
        try:
            config_file = os.path.join(project_dir, config_file)
            with codecs.open(config_file, encoding='utf-8-sig') as f:
                self.cf.readfp(f)
        except IOError:
            raise IOError

    def get(self, option, section='DEFAULT'):
        return self.cf.get(section, option)   # todo try ..


if __name__ == '__main__':
    cf = Config()
    print(cf.get('url_list_file'))