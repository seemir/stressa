# -*- coding: utf-8 -*-
"""
Implementation of connector against Finn.no housing ownership history search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json
from time import time
from http.client import responses

import pandas as pd
import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

import json_repair
from bs4 import BeautifulSoup
from pandas import DataFrame

from source.util import LOGGER, TimeOutError, NoConnectionError, Tracking, \
    InvalidData

from source.domain import Money

from source.app.connectors.settings import FINN_OWNER_URL, TIMEOUT
from source.app.connectors.finn import Finn


class FinnOwnership(Finn):
    """
    Connector that retrieves housing ownership history from Finn.no given a Finn-code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to search finn ownership history information for

        """
        super().__init__(finn_code=finn_code)

    @Tracking
    def ownership_response(self):
        """
        Response from Finn-no housing ownership history search

        Returns
        -------
        our     : requests.models.Response
                  response with housing ownership information

        """
        try:
            try:
                start = time()
                owner_response = requests.get(
                    FINN_OWNER_URL + "{}".format(self.finn_code),
                    timeout=TIMEOUT)
                owner_status_code = owner_response.status_code
                elapsed = self.elapsed_time(start)
                status_msg = "HTTP status code -> OWNERSHIP HISTORY: [{}: {}] -> elapsed: {}".format(
                    owner_status_code, responses[owner_status_code],
                    elapsed)

                if owner_status_code >= 500:
                    LOGGER.error(status_msg)
                    raise ConnectError(status_msg)

                LOGGER.info(status_msg)
                return owner_response
            except ConnectTimeout as finn_owner_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or "
                    "contact system administrator, exited with '{}'".format(
                        finn_owner_timeout_error))
        except ConnectError as finn_owner_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    finn_owner_response_error))

    @Tracking
    def housing_ownership_information(self):
        """
        Retrieve and parse housing ownership history information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            LOGGER.info(
                "trying to retrieve 'housing_ownership_information' for -> '{}'".format(
                    self.finn_code))

            response = self.ownership_response()

            if not response:
                raise InvalidData(
                    "[{}] Not found! '{}' may be an invalid Finn code".format(
                        self.__class__.__name__, self.finn_code))

            owner_soup = BeautifulSoup(response.content,
                                       "lxml")

            # with open('content.html', 'w', encoding='utf-8') as file:
            #     file.write(owner_soup.prettify())

            info = {}
            script_tag = None
            history_data = None

            for script in owner_soup.find_all('script'):
                if 'window.__remixContext' in script.text:
                    script_tag = script.text

            if script_tag:
                cleaned_script = (script_tag
                                  .replace(r'\u003e', '>')
                                  .replace(r'\u003c', '<')
                                  .replace(r'\u0026', '&')
                                  .replace(r'\n', '')
                                  .replace(r'\R', 'R'))

                cleaned_script = " ".join(cleaned_script.split()).replace(
                    'window.__remixContext = ', '')[:-1]

                cleaned_script = dict(json_repair.loads(cleaned_script))

                if 'state' in cleaned_script:
                    state = cleaned_script['state']
                    if 'loaderData' in state:
                        loader_data = state['loaderData']
                        if 'routes/realestate+/_common+/ownershiphistory[.html]' in loader_data:
                            routes = loader_data[
                                'routes/realestate+/_common+/ownershiphistory[.html]']
                            if 'historyData' in routes:
                                history_data = routes['historyData']

            if history_data:
                registration_date = []
                property_type = []
                property_id = []
                amount = []

                for ownership_element in history_data:
                    if 'data' in ownership_element:
                        ownership_data_element = ownership_element['data']
                        for element in ownership_data_element:
                            name = element['name']
                            if name == 'registrationDate':
                                registration_date.append(element['value'][0:10])
                            if name == 'propertyType':
                                property_type.append(element['value'])
                            if name == 'sectionNumber' and element[
                                'value'] != 0:
                                property_id.append(str(element['value']))
                            elif name == 'shareNumber' and element[
                                'value'] != 0:
                                property_id.append(str(element['value']))
                            if name == 'amount':
                                amount.append(
                                    Money(str(element['value'])).value())

                ownership_data = {'Tinglyst': registration_date,
                                  'Boligtype': property_type,
                                  'Boligidentifikasjon': property_id,
                                  'Pris': amount}
                info.update({'historikk': ownership_data})

                LOGGER.success(
                    "'housing_ownership_information' successfully retrieved")
                return info
            else:
                raise ValueError('No ownership history found')

        except Exception as invalid_data_exception:
            raise InvalidData(
                "Something went wrong, exited with '{}'".format(
                    invalid_data_exception))

    @Tracking
    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save ownership information to JSON file

        """
        self.save_json(self.housing_ownership_information(), file_dir,
                       file_prefix="HousingOwnershipInfo_")

        LOGGER.success(
            "'housing_ownership_information' successfully parsed to JSON at '{}'".format(
                file_dir))

# if __name__ == '__main__':
#     finn_ad = FinnOwnership('371008605')
#     print(finn_ad.housing_ownership_information())
