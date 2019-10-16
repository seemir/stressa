# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from loguru import logger
import os


def loggr(file_path=None):
    """
    loguru logger method that produces one logger per. call to method

    Parameters
    ----------
    file_path    : str
                   file path to store all .log files, default is __file__, i.e.
                   directory  from which the call to the method was invoked

    Returns
    -------
    out     : loguru._logger.Logger

    """
    try:
        f = __file__ if not file_path else file_path
        log_dir = os.path.dirname(f) + "/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logger.add(log_dir + "/application.log")
        return logger
    except Exception as e:
        raise OSError("an error occurred with: {}".format(e))


main_logger = loggr()
