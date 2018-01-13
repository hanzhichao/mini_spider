#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_urls(seed_file):
    """
    get urls from seed file,a new blank line needed at the end of the file
    @:param seed_file type:str seed_file path, read from the config file
    """
    with open(seed_file, 'r') as f:
        # remove '\n' at the end of each line and add 'http://' if url not contains 'http'
        return map(lambda x: 'http://' + x[:-1] if 'http' not in x else x[:-1], f.readlines())

