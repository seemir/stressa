# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.settings import portalen_url, portalen_cred
from source.log import main_logger
from bs4 import BeautifulSoup
from .scraper import Scraper
import requests
import os


class Portalen(Scraper):
    """
    Scraper that scrapes information from finansportalen.no mortgage
    applications calculator

    """

    def __init__(self):
        """
        Constructor / Instantiate the class

        """
        super().__init__()
        try:
            self.browser = requests.post(portalen_url, auth=portalen_cred)
        except Exception as exp:
            main_logger.exception(exp)
            raise exp

    def response(self):
        """
        Response from finansportalen.no xml feed

        Returns
        -------
        our     : requests.models.Response
                  response with mortgage information

        """
        return self.browser

    def mortgage_offers(self):
        """
        Retrieve finansportalen.no's boliglån grunndata xml and stores it locally directory

        """
        try:
            soup = BeautifulSoup(self.response().content, "lxml")
            file_dir = os.path.dirname(__file__) + "/xml"
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(file_dir + '/portalen_data.xml', 'w') as f:
                f.write(soup.prettify())
        except Exception as exp:
            main_logger.exception(exp)
            raise exp
