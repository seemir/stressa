# -*- coding: utf-8 -*-
"""
Implementation of connector against Finn.no housing statistics search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import base64
from time import time
from typing import Union
from datetime import datetime

import json
from http.client import responses

import asyncio
from asyncio import TimeoutError as TError
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectionError

from bs4 import BeautifulSoup
import numpy as np
import json_repair

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor, Tracking
from source.domain import Amount, Money

from source.app.connectors.settings import FINN_STAT_URL, TIMEOUT
from source.app.connectors.finn import Finn


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
            info = {}
            stat_soup = BeautifulSoup(response, "lxml")

            # with open('content.html', 'w', encoding='utf-8') as file:
            #     file.write(stat_soup.prettify())

            info = {}
            price_statistics = None
            script_tag = None

            sqm_price = ''
            clicks = ''
            entity_variable = ''
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
                            sqm_price = Money(str(price_statistics_data['sqmPrice'])).value()

                        if 'clicks' in price_statistics_data:
                            clicks = Amount(str(price_statistics_data['clicks'])).amount

                        if 'realEstateSalesData' in price_statistics_data:
                            real_estate_sales_data = price_statistics_data['realEstateSalesData']

                            if len(real_estate_sales_data) == 2 and real_estate_sales_data:

                                for i, entity in enumerate(real_estate_sales_data):

                                    entity_area_data = real_estate_sales_data[i]

                                    if i == 0:
                                        entity_variable = entity_variable
                                        entity_name = 'city_area_sqm_price'
                                        area_details = {
                                            'city_area': entity_area_data['locationDetails']}
                                    elif i == 1:
                                        entity_variable = municipality_sqm_price
                                        entity_name = 'municipality_sqm_price'
                                        area_details = {
                                            'municipality': entity_area_data['locationDetails']}
                                    else:
                                        break

                                    if 'histData' in entity_area_data:

                                        entity_area_history_data = {}
                                        entity_area_hist_data = entity_area_data['histData']

                                        for price_info in entity_area_hist_data:
                                            entity_sqm_price = price_info['sqmPrice']
                                            entity_number_of_sales = price_info['numberOfSales']
                                            entity_area_history_data.update(
                                                {entity_sqm_price: entity_number_of_sales})

                                        entity_variable = self.calculate_average(
                                            entity_area_history_data)

                                    info.update(area_details)
                                    info.update({entity_name: Money(entity_variable).value()})

                info.update({'sqm_price': sqm_price,
                             'views': clicks})

                LOGGER.success("'housing_stat_information' successfully retrieved")

                return info
            else:
                raise ValueError('No ad statistics found')

            # stat_data = json.loads(
            #     stat_soup.find("script", attrs={"type": "application/json"}).contents[0])
            #
            # optional_sqm_price = [str(value.get_text()).replace(u"\xa0", "") for
            #                       value in stat_soup.find_all("strong",
            #                                                   attrs={"style": "min-width:10px"})]
            #
            # info.update(self.extract_sqm_price(stat_data, info, optional_sqm_price))
            # info.update(self.extract_view_statistics(stat_data, info))
            # info.update(self.extract_published_statistics(stat_data, info))
            # info.update(self.extract_area_sales_statistics(stat_data, info))
            # info.update(self.calculate_sqm_price_areas(info))
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
    def extract_area_sales_statistics(self, areal_sales_statistics: dict, info: dict):
        """
        method for extracting the detail view statistics

        Parameters
        ----------
        areal_sales_statistics  : dict
                                  dictionary with area sales statistics
        info                    : dict
                                  dictionary to store results

        Returns
        -------
        out                     : dict
                                  dictionary with results

        """
        Assertor.assert_data_types([areal_sales_statistics, info], [dict, dict])
        historical_data_names = ["hist_data_city_area", "hist_data_municipality"]
        location_name = ["city_area", "municipality"]
        for prop, value in areal_sales_statistics.items():
            if prop.lower() == 'props':
                for pro, val in value.items():
                    if pro.lower() == 'pageprops':
                        for pr_name, vl_name in val.items():
                            if pr_name.lower() == 'locationhistory':
                                for i, data in enumerate(vl_name):
                                    if len(areal_sales_statistics) == 3:
                                        if i == 0:
                                            continue
                                        i -= 1
                                    for prop_val, value_name in data.items():
                                        if prop_val.lower() == "locationdetails":
                                            if value_name:
                                                if "name" in value_name[0]:
                                                    info.update(
                                                        {location_name[i]: value_name[0]["name"]})
                                        elif prop_val.lower() == "histdata":
                                            historical_values = {}
                                            for ke_val, va_name in value_name.items():
                                                historical_values.update(
                                                    {int(ke_val): int(va_name)})
                                            info.update(
                                                {historical_data_names[i]: historical_values})
                                            info.update(
                                                {historical_data_names[i] + "_count": Amount(
                                                    str(sum(historical_values.values()))).amount})
        if all(name in info.keys() for name in historical_data_names):
            self.harmonize_data_sets(info)
        return info

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

# if __name__ == '__main__':
#     finn_stat = FinnStat('357198989')
#
#     print(finn_stat.housing_stat_information())
