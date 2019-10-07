# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.exception.base_class_cannot_be_instantiated import BaseClassCannotBeInstantiated
from source.util.assertor import Assertor
from mechanize import Browser
import datetime
import json
import os


class ApiQuery:
    """
    Apu Query superclass

    """

    @staticmethod
    def _to_json(file_dict: dict, file_dir="report/json", file_title="Info"):
        """
        save information in object to JSON file

        Parameters
        ----------
        file_dict   : dict
                      retrieve information from this object and save to file
        file_dir    : str
                      file directory to save JSON files
        file_title  : str
                      title of file

        """
        Assertor.assert_date_type({file_dict: dict, file_dir: str, file_title: str})

        try:
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
        except Exception as e:
            raise OSError("creation of dir " + file_dir + " failed with: " + str(e))

        js = json.dumps(file_dict, indent=2, separators=(',', ': '),
                        ensure_ascii=False)
        local_time = datetime.datetime.now().isoformat().replace(":", "-").replace(".", "-")
        file = open(os.path.join(file_dir, file_title + local_time + ".json"), "w")
        file.write(js)
        file.close()

    def __init__(self):
        """
        Abstract class, so class cannot be instantiated

        """
        if type(self) == ApiQuery:
            raise BaseClassCannotBeInstantiated(
                "base class '{}' cannot be instantiated".format(self.__class__.__name__))

        self.browser = Browser()
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(False)
