# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from loguru import logger
import os

try:
    log_dir = os.path.dirname(__file__) + "/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    formatter = "[{time:DD-MM-YYYY at HH:mm:ss}](elapsed: {elapsed}) | {level} | {name} | {message}"
    logger.add(log_dir + "/application.log", format=formatter)
except Exception as e:
    raise OSError("an error occurred with: {}".format(e))
