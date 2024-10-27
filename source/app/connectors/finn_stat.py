# -*- coding: utf-8 -*-
"""
Implementation of connector against Finn.no housing statistics search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import base64
from time import time

from http.client import responses

import asyncio
from asyncio import TimeoutError as TError
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectionError

from bs4 import BeautifulSoup
import numpy as np
import json_repair

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor, Tracking
from source.domain import Amount

from .settings import FINN_STAT_URL, TIMEOUT
from .finn import Finn


class FinnStat(Finn):
    """
    Connector that retrieves housing statistics information from Finn.no given a Finn-code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to search finn statistics for

        """
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(finn_code=finn_code)

    @Tracking
    async def stat_response(self):
        """
        Response from Finn-no housing statistics search

        Returns
        -------
        our     : requests.models.Response
                  response with housing statistics information

        """
        try:
            try:
                start = time()
                async with ClientSession(timeout=ClientTimeout(TIMEOUT)) as session:
                    async with session.get(
                            FINN_STAT_URL + "{}".format(self.finn_code)) as stat_response:
                        stat_status_code = stat_response.status
                        elapsed = self.elapsed_time(start)
                        LOGGER.info(
                            "HTTP status code -> STATISTICS: [{}: {}] -> elapsed: {}".format(
                                stat_status_code, responses[stat_status_code], elapsed))
                        return await stat_response.content.read()
            except TError:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator")
        except ClientConnectionError as finn_stat_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    finn_stat_response_error))

    @Tracking
    def housing_stat_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict

        """
        LOGGER.info(
            "trying to retrieve 'housing_stat_information' for -> '{}'".format(self.finn_code))
        response = asyncio.run(self.stat_response())
        try:
            stat_soup = BeautifulSoup(response, "lxml")

            info = {}
            price_statistics = None
            script_tag = None

            sqm_price = ''
            clicks = ''
            dimension_sqm_price = ''
            municipality_sqm_price = ''

            for script in stat_soup.find_all('script'):
                if 'window.__remixContext' in script.text:
                    script_tag = script.text

            if script_tag:

                cleaned_script = " ".join(script_tag.split()).replace(
                    'window.__remixContext = ', '')[:-1]

                cleaned_script = dict(json_repair.loads(cleaned_script))

                if 'state' in cleaned_script:
                    state = cleaned_script['state']
                    if 'loaderData' in state:
                        loader_data = state['loaderData']
                        if 'routes/prisstatistikk.$adId' in loader_data:
                            routes = loader_data['routes/prisstatistikk.$adId']
                            if 'priceStatistic' in routes:
                                price_statistic = routes['priceStatistic']
                                if 'content' in price_statistic:
                                    price_statistics = price_statistic['content']

            if price_statistics:

                price_statistics_soup = BeautifulSoup(price_statistics, 'lxml')

                base64_price_json = price_statistics_soup.find(
                    'div', attrs={'data-props': True})['data-props']

                decoded_price_json = base64.b64decode(base64_price_json)
                decoded_price_json_string = json_repair.loads(
                    decoded_price_json.decode('utf-8'))

                if 'response' in decoded_price_json_string:

                    response = dict(decoded_price_json_string['response'])

                    if response['status'] == 200:

                        price_statistics_data = response['data']

                        if 'sqmPrice' in price_statistics_data:
                            sqm_price = Amount(str(price_statistics_data['sqmPrice'])).amount

                        if 'clicks' in price_statistics_data:
                            clicks = Amount(str(price_statistics_data['clicks'])).amount

                        if 'realEstateSalesData' in price_statistics_data:
                            real_estate_sales_data = price_statistics_data['realEstateSalesData']

                            if len(real_estate_sales_data) == 2 and real_estate_sales_data:

                                for i, entity in enumerate(real_estate_sales_data):

                                    dimension_count = 0
                                    dimension_history_data = {}
                                    dimension_data = real_estate_sales_data[i]

                                    if i == 0:
                                        dimension_sqm_price = dimension_sqm_price
                                        dimension_sqm_price_name = 'city_area_sqm_price'
                                        dimension_area_details = {
                                            'city_area': dimension_data['locationDetails']}
                                        dimension_count_name = 'hist_data_city_area_count'
                                        dimension_area_hist_data_name = 'hist_data_city_area'
                                    elif i == 1:
                                        dimension_sqm_price = municipality_sqm_price
                                        dimension_sqm_price_name = 'municipality_sqm_price'
                                        dimension_area_details = {
                                            'municipality': dimension_data['locationDetails']}
                                        dimension_count_name = 'hist_data_municipality_count'
                                        dimension_area_hist_data_name = 'hist_data_municipality'
                                    else:
                                        break

                                    if 'histData' in dimension_data:

                                        entity_area_hist_data = dimension_data['histData']

                                        for price_info in entity_area_hist_data:
                                            entity_sqm_price = price_info['sqmPrice']
                                            entity_number_of_sales = price_info['numberOfSales']
                                            entity_sales_count = price_info['numberOfSales']
                                            dimension_history_data.update(
                                                {entity_sqm_price: entity_number_of_sales})
                                            dimension_count += entity_sales_count

                                        dimension_sqm_price = self.calculate_average(
                                            dimension_history_data)

                                    info.update(dimension_area_details)
                                    info.update(
                                        {dimension_sqm_price_name: dimension_sqm_price + " kr/m²"})
                                    info.update(
                                        {dimension_count_name: Amount(str(dimension_count)).amount})
                                    info.update(
                                        {dimension_area_hist_data_name: dimension_history_data})

                info.update({'sqm_price': sqm_price + " kr/m²",
                             'views': clicks})

                historical_data_names = ["hist_data_city_area", "hist_data_municipality"]
                if all(name in info.keys() for name in historical_data_names):
                    self.harmonize_data_sets(info)

                LOGGER.success("'housing_stat_information' successfully retrieved")

                return info
            else:
                raise ValueError('No ad statistics found')

        except Exception as no_ownership_history_exception:
            LOGGER.debug("[{}] No housing statistics found!, exited with '{}'".format(
                self.__class__.__name__, no_ownership_history_exception))

    @Tracking
    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save statistics information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.housing_stat_information(), file_dir, file_prefix="HousingStatInfo_")
        LOGGER.success(
            "'housing_stat_information' successfully parsed to JSON at '{}'".format(file_dir))

    @Tracking
    def calculate_sqm_price_areas(self, info: dict):
        """
        method for calculating sqm price in city area and municipality

        Parameters
        ----------
        info                    : dict
                                  dictionary to store results

        """
        Assertor.assert_data_types([info], [dict])
        if all(name in info.keys() for name in ["hist_data_city_area",
                                                "hist_data_municipality"]):
            info.update(
                {"city_area_sqm_price": self.calculate_average(
                    info["hist_data_city_area"]) + " kr/m²"})
            info.update({"municipality_sqm_price": self.calculate_average(
                info["hist_data_municipality"]) + " kr/m²"})
            return info

    @Tracking
    def harmonize_data_sets(self, info):
        """
        method for harmonize data sets

        Parameters
        ----------
        info                    : dict
                                  dictionary to store results
        Returns
        -------
        out                     : dict
                                  dictionary with results

        """
        if sum(list(info["hist_data_municipality"].values())) > 15000:
            mean = np.nanmean(list(info["hist_data_municipality"].keys()))
            std = np.nanstd(list(info["hist_data_municipality"].keys()))
            upper = mean + std * 1.5
            lower = mean - std * 1.5
            for key, val in info["hist_data_municipality"].copy().items():
                if lower <= key <= upper:
                    info["hist_data_municipality"].update({key: val})
                else:
                    info["hist_data_municipality"].pop(key)
        city_area_values = {}
        for key in info["hist_data_municipality"].keys():
            if key not in info["hist_data_city_area"].keys():
                city_area_values.update({key: 0})
            else:
                city_area_values.update({key: info["hist_data_city_area"][key]})
        info.update({"hist_data_city_area": city_area_values})

    @Tracking
    def calculate_average(self, elements: dict):
        """
        method for calculating the average

        Parameters
        ----------
        elements      : dict
                        dictionary of prices

        Returns
        -------
        out           : str
                        string with results

        """
        products = []
        sums = 0
        for price, num in elements.items():
            products.append(int(price) * num)
            sums += num
        average = Amount(str(round(sum(products) / sums))).amount if sums != 0 else "0"
        return average
