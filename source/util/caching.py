# -*- coding: utf-8 -*-

"""
Caching module for all responses from external systems

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os

import requests_cache

from .assertor import Assertor


def cache(file_path: str, file_name: str):
    """
    caching method for requests package, i.e. all responses using the
    requests package gets stored to local

    Parameters
    ----------
    file_path   : str
                  file path to store db files
    file_name   : str
                  name of db file

    """
    try:
        Assertor.assert_data_types([file_path, file_name], [(type(None), str), str])
        file = __file__ if not file_path else file_path
        cache_dir = os.path.join(os.path.dirname(file), "temp")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        cache_db = os.path.join(cache_dir, file_name)
        requests_cache.install_cache(cache_db)
    except Exception as log_exception:
        raise OSError("an error occurred with: {}".format(log_exception))
