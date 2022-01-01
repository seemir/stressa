# -*- coding: utf-8 -*-

"""
Implementation of scaper against Skatteetaten tax calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from typing import Union

import json
from http.client import responses

import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from source.util import Assertor, LOGGER, NoConnectionError, TimeOutError, Tracking

from source.app.scrapers.settings import SKATTEETATEN_URL, TIMEOUT
from source.app.scrapers import Scraper


class Skatteetaten(Scraper):
    """
    Class that produces estimated total Taxes for a given year

    """

    def __init__(self, age: Union[str, int], income: Union[str, int, float]):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        age         : str, int
                      age of individual
        income      : str, int, float
                      income of individual

        """

        try:
            super().__init__()
            Assertor.assert_data_types([age, income], [(str, int), (str, int, float)])

            self.age = str(age + 1)
            self.income = str(income)
            self.year = str(2022)
            self.url = SKATTEETATEN_URL + self.year

            LOGGER.success(
                "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_))
        except Exception as skatteetaten_exception:
            LOGGER.exception(skatteetaten_exception)
            raise skatteetaten_exception

    @Tracking
    def payload(self):
        """
        method for generating payload str

        """
        with open(os.path.dirname(__file__) + '\\payloads\\skatteetaten_payload.json') as json_file:
            json_data = json.load(json_file)
        return json.dumps(json_data) \
            .replace("loennsinntektNaturalytelseMvBelop", self.income) \
            .replace("alderIInntektsaarVerdi", self.age)

    @Tracking
    def response(self):
        """
        submits and gets response for skatteetaten request

        Returns
        -------
        out     : requests.models.Response
                  response with interest rate information

        """
        try:
            try:
                response = requests.post(url=self.url, data=self.payload(), timeout=TIMEOUT)
                status_code = response.status_code
                LOGGER.info(
                    "HTTP status code -> [{}: {}]".format(status_code, responses[status_code]))
                return response
            except ConnectTimeout as ssb_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system administrator, "
                    "exited with '{}'".format(ssb_timeout_error))
        except ConnectError as ssb_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    ssb_response_error))

    @Tracking
    def tax_information(self):
        """
        method for getting tax dict given information passed to class

        Returns
        -------
        out     : dict
                  tax information given information passed through class

        """
        tax_dict = self.response().json()
        tax_info = {}

        for keys, values in tax_dict.items():
            if keys == "hovedperson":
                for key, value in values.items():
                    if key == "beregnetSkattV4":
                        for tag, val in value.items():
                            if tag == "skatteklasse":
                                tax_info.update({tag: val})
                            elif tag == "skatteregnskapskommune":
                                tax_info.update({tag: val})
                            elif tag == "informasjonTilSkattelister":
                                tax_info.update({"nettoinntekt": str(val["nettoinntekt"])})
                                tax_info.update({"nettoformue": str(val["nettoformue"])})
                                tax_info.update({"beregnetSkatt": str(val["beregnetSkatt"])})
                            elif tag == "beregnetSkattFoerSkattefradrag":
                                tax_info.update(
                                    {tag: {"grunnlag": str(val["grunnlag"]),
                                           "beloep": str(val["beloep"])}})
                            elif tag == "beregnetSkatt":
                                tax_info.update(
                                    {tag: {"grunnlag": str(val["grunnlag"]),
                                           "beloep": str(val["beloep"])}})
                            elif tag == "skattOgAvgift":
                                for sub_tag, sub_val in val.items():
                                    if sub_tag in ["formuesskattTilStat",
                                                   "inntektsskattTilKommune",
                                                   "inntektsskattTilFylkeskommune",
                                                   "inntektsskattTilKommuneOgFylkeskommune",
                                                   "formuesskattTilKommune",
                                                   "fellesskatt", "trinnskatt",
                                                   "trygdeavgiftAvLoennsinntekt",
                                                   "sumTrygdeavgift"]:
                                        tax_info.update(
                                            {sub_tag: {"grunnlag": str(sub_val["grunnlag"]),
                                                       "beloep": str(sub_val["beloep"])}})
                    elif key == "beregningsgrunnlagV4":
                        for tag, val in value.items():
                            if tag == "beregningsgrunnlagsobjekt":
                                for element in val:
                                    tax_info.update(
                                        {element["tekniskNavn"]: str(element["beloep"])})
                    elif key == "summertSkattegrunnlagForVisningV7":
                        for tag, val in value.items():
                            if tag == "skattegrunnlagsobjekt":
                                for element in val:
                                    tax_info.update(
                                        {element["tekniskNavn"]: str(element["beloep"])})
        return tax_info


skatteetaten = Skatteetaten(32, 671000)

print(skatteetaten.tax_information())
