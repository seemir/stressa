# -*- coding: utf-8 -*-
"""
Implementation of scarper against Finn.no housing statistics search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from datetime import datetime
from time import time

import json
from http.client import responses

import asyncio
from asyncio import TimeoutError as TError
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientConnectionError

from bs4 import BeautifulSoup
import numpy as np

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor, Tracking
from source.domain import Amount

from .settings import FINN_STAT_URL, TIMEOUT
from .finn import Finn


class FinnStat(Finn):
    """
    Scraper that scrapes housing statistics information from Finn.no given a Finn-code

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

            sq_price = \
                json.loads(stat_soup.find("script", attrs={"id": "area-prices"}).contents[0])[
                    "price"]

            info.update({"sqm_price": Amount(str(sq_price)).amount + " kr/m²"})

            view_statistics_total = json.loads(
                stat_soup.find("script", attrs={"id": "ad-summary"}
                               ).contents[0])[self.finn_code]
            view_statistics_detail = json.loads(
                stat_soup.find("script", attrs={"id": "ad"}).contents[0])
            area_sales_statistics = json.loads(
                stat_soup.find("script", attrs={"id": "area-sales"}).contents[0])

            info.update(self.extract_view_statistics(view_statistics_total, info))
            info.update(self.extract_detail_view_statistics(view_statistics_detail, info))
            info.update(self.extract_area_sales_statistics(area_sales_statistics, info))

            if all(name in info.keys() for name in ["hist_data_city_area",
                                                    "hist_data_municipality"]):
                info.update(
                    {"city_area_sqm_price": self.calculate_average(
                        info["hist_data_city_area"]) + " kr/m²"})
                info.update({"municipality_sqm_price": self.calculate_average(
                    info["hist_data_municipality"]) + " kr/m²"})

            # with open('stat_data.json', 'w', encoding='utf-8') as file:
            #     json.dump(info, file, ensure_ascii=False, indent=4)

            LOGGER.success("'housing_stat_information' successfully retrieved")

            return info
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
    def extract_view_statistics(self, total_view_statistics: dict, info: dict):
        """
        method for extracting the total view statistics

        Parameters
        ----------
        total_view_statistics   : dict
                                  dictionary with view statistics
        info                    : dict
                                  dictionary to store results

        Returns
        -------
        out                     : dict
                                  dictionary with results

        """
        Assertor.assert_data_types([total_view_statistics, info], [dict, dict])
        for prop, value in total_view_statistics.items():
            if isinstance(value, (int, float)):
                info.update({prop.lower(): Amount(str(value)).amount})
        return info

    @Tracking
    def extract_detail_view_statistics(self, detail_view_statistics: dict, info: dict):
        """
        method for extracting the detail view statistics

        Parameters
        ----------
        detail_view_statistics  : dict
                                  dictionary with detailed view statistics
        info                    : dict
                                  dictionary to store results

        Returns
        -------
        out                     : dict
                                  dictionary with results

        """
        Assertor.assert_data_types([detail_view_statistics, info], [dict, dict])
        for prop, value in detail_view_statistics.items():
            if prop.lower() == "ad":
                if "firstPublished" in value.keys():
                    pub = datetime.fromisoformat(value["firstPublished"][:-1])
                    date = datetime.strptime(str(pub), "%Y-%m-%d %H:%M:%S").strftime(
                        "%d. %b %Y %H:%M")
                    info.update(
                        {"first_published": str(date).lower() + " ({} dager siden)".format(
                            (datetime.today() - pub).days)})
                    info.update({
                        "published": datetime.strptime(str(pub), "%Y-%m-%d %H:%M:%S").strftime(
                            "%d.%m.%Y")})
            elif prop.lower() == "views":
                organic = {}
                effect = {}
                total = {}
                views_development = {"views_development": {}}
                for key, val in value.items():
                    if len(val) == 2:
                        effect.update({key: list(val.values())[0]})
                        organic.update({key: list(val.values())[1]})
                        total.update({key: list(val.values())[0] + list(val.values())[1]})
                    elif len(val) == 1:
                        effect.update({key: 0})
                        organic.update({key: list(val.values())[0]})
                        total.update({key: list(val.values())[0]})
                    else:
                        effect.update({key: 0})
                        organic.update({key: 0})
                        total.update({key: 0})

                views_development["views_development"].update(
                    {"dates": list(dict(sorted(organic.items())).keys())})
                views_development["views_development"].update(
                    {"organic_views": list(dict(sorted(organic.items())).values())})
                views_development["views_development"].update(
                    {"effect_views": list(dict(sorted(effect.items())).values())})
                views_development["views_development"].update(
                    {"total_views": list(dict(sorted(total.items())).values())})
                info.update(views_development)

            elif prop.lower() == "totals":
                for key, val in value.items():
                    info.update({key.lower(): Amount(str(val)).amount})
            elif prop.lower() == "performance":
                if "description" in value.keys():
                    for key, val in value["description"].items():
                        if key.lower() == "price":
                            info.update(
                                {"price_range": val.replace("kr\xa0", "").replace(",00",
                                                                                  " kr").strip()})
                        elif key.lower() == "published":
                            pass
                        elif key.lower() == "size":
                            info.update({"size_range": val.replace(" -", " m² -") + " m²"})
                        else:
                            info.update({key.lower(): val})
        return info

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
        Assertor.assert_data_types([areal_sales_statistics, info], [list, dict])
        historical_data_names = ["hist_data_city_area", "hist_data_municipality"]
        location_name = ["city_area", "municipality"]
        for i, data in enumerate(areal_sales_statistics):
            if len(areal_sales_statistics) == 3:
                if i == 0:
                    continue
                i -= 1
            for prop, value in data.items():
                if prop.lower() == "locationdetails":
                    if value:
                        if "name" in value[0]:
                            info.update({location_name[i]: value[0]["name"]})
                elif prop.lower() == "histdata":
                    historical_values = {}
                    for key, val in value.items():
                        historical_values.update({int(key): int(val)})
                    info.update({historical_data_names[i]: historical_values})
                    info.update(
                        {historical_data_names[i] + "_count": Amount(
                            str(sum(historical_values.values()))).amount})
            if all(name in info.keys() for name in historical_data_names):
                self.harmonize_data_sets(info)
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
            mean = np.mean(list(info["hist_data_municipality"].keys()))
            std = np.std(list(info["hist_data_municipality"].keys()))
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
