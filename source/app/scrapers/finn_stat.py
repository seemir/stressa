# -*- coding: utf-8 -*-
"""
Implementation of scarper against Finn.no housing statistics search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from datetime import datetime

import json
from http.client import responses
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError
import requests

from bs4 import BeautifulSoup

from source.util import LOGGER, TimeOutError, NoConnectionError, Assertor
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

    def stat_response(self):
        """
        Response from Finn-no housing statistics search

        Returns
        -------
        our     : requests.models.Response
                  response with housing statistics information

        """
        try:
            try:
                stat_response = requests.get(FINN_STAT_URL + "{}".format(self.finn_code),
                                             timeout=TIMEOUT)
                stat_status_code = stat_response.status_code
                LOGGER.info(
                    "HTTP status code -> STATISTICS: [{}: {}]".format(stat_status_code,
                                                                      responses[stat_status_code]))
                return stat_response
            except ConnectTimeout as finn_stat_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "\nexited with '{}'".format(finn_stat_timeout_error))
        except ConnectError as finn_stat_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator,\nexited with '{}'".format(
                    finn_stat_response_error))

    def housing_stat_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict

        """
        try:
            LOGGER.info(
                "trying to retrieve '{}' for -> '{}'".format(self.housing_stat_information.__name__,
                                                             self.finn_code))
            response = self.stat_response()
            info = {}
            try:
                stat_soup = BeautifulSoup(response.content, "lxml")
                sq_price = json.loads(stat_soup.find("script", attrs={"id": "area-prices"}).text)[
                    "price"]
                info.update({"sqm_price": Amount.format_amount(sq_price) + " kr/m²"})

                view_statistics_total = json.loads(
                    stat_soup.find("script", attrs={"id": "ad-summary"}).text)[self.finn_code]
                view_statistics_detail = json.loads(
                    stat_soup.find("script", attrs={"id": "ad"}).text)
                area_sales_statistics = json.loads(
                    stat_soup.find("script", attrs={"id": "area-sales"}).text)

                # with open('statistics.json', 'w', encoding='utf-8') as f:
                #     json.dump(view_statistics_total, f, ensure_ascii=False, indent=4)

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

                LOGGER.success(
                    "'{}' successfully retrieved".format(self.housing_stat_information.__name__))
                return info
            except AttributeError as no_ownership_history_exception:
                LOGGER.debug("No housing statistics found!, exited with '{}'".format(
                    no_ownership_history_exception))
        except Exception as housing_stat_information_exception:
            LOGGER.exception(housing_stat_information_exception)
            raise housing_stat_information_exception

    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save statistics information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.housing_stat_information(), file_dir, file_prefix="HousingStatInfo_")
        LOGGER.success(
            "'housing_stat_information' successfully parsed to JSON at '{}'".format(file_dir))

    @staticmethod
    def extract_view_statistics(total_view_statistics: dict, info: dict):
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
                unique_keys = {"totalviews": "views", "latestemailcount": "email_sent",
                               "currentfavorites": "favorite_click"}
                if prop.lower() in unique_keys.keys():
                    info.update({unique_keys[prop.lower()]: Amount.format_amount(str(value))})
                else:
                    info.update({prop.lower(): Amount.format_amount(str(value))})
        return info

    @staticmethod
    def extract_detail_view_statistics(detail_view_statistics: dict, info: dict):
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
                    today = datetime.today()
                    pub = datetime.fromisoformat(value["firstPublished"][:-1])
                    days = today - pub
                    date = datetime.strptime(str(pub), "%Y-%m-%d %H:%M:%S").strftime(
                        "%d. %b %Y %H:%M")
                    info.update(
                        {"first_published": str(date).lower() + " ({} dager siden)".format(
                            days.days)})
                    info.update({
                        "published": datetime.strptime(str(pub), "%Y-%m-%d %H:%M:%S").strftime(
                            "%d.%m.%Y")})
            elif prop.lower() == "views":
                info.update({"views_development": value})
            elif prop.lower() == "totals":
                for key, val in value.items():
                    info.update({key.lower(): Amount.format_amount(val)})
            elif prop.lower() == "performance":
                if "description" in value.keys():
                    for key, val in value["description"].items():
                        if key.lower() == "price":
                            info.update(
                                {"price_range": val.replace("kr ", "").replace(",00", " kr")})
                        elif key.lower() == "published":
                            pass
                        elif key.lower() == "size":
                            info.update({"size_range": val.replace(" -", " m² -") + " m²"})
                        else:
                            info.update({key.lower(): val})
            else:
                pass
        return info

    @staticmethod
    def extract_area_sales_statistics(areal_sales_statistics: dict, info: dict):
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
        historical_data_names = ["hist_data_city_area", "hist_data_municipality"]
        location_name = ["city_area", "municipality"]
        Assertor.assert_data_types([areal_sales_statistics, info], [list, dict])
        for i, data in enumerate(areal_sales_statistics):
            for prop, value in data.items():
                if prop.lower() == "locationdetails":
                    if value:
                        if "name" in value[0]:
                            info.update({location_name[i]: value[0]["name"]})
                elif prop.lower() == "histdata":
                    info.update({historical_data_names[i]: value})
                else:
                    pass
        return info

    @staticmethod
    def calculate_average(elements: dict):
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
        return Amount.format_amount(str(round(sum(products) / sums)))
