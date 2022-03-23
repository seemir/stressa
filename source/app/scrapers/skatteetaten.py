# -*- coding: utf-8 -*-

"""
Implementation of scaper against Skatteetaten tax calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
from typing import Union

from http.client import responses
from datetime import date

import json
import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from source.util import Assertor, LOGGER, NoConnectionError, TimeOutError, Tracking

from source.app.scrapers.settings import SKATTEETATEN_URL, TIMEOUT
from source.app.scrapers import Scraper

from source.domain import Money


class Skatteetaten(Scraper):
    """
    Class that produces estimated total Taxes for a given year

    """

    tax_version_mapping = {'2022': ('skatteberegningsgrunnlagV7', 'skattepliktV9'),
                           '2021': ('skatteberegningsgrunnlagV6', 'skattepliktV8'),
                           '2020': ('skattegrunnlagV6', 'skattepliktV7'),
                           '2019': ('skattegrunnlagV5', 'skattepliktV6'),
                           '2018': ('skattegrunnlagV5', 'skattepliktV5')}

    def __init__(self, age: Union[str, int], income: Union[str, int, float],
                 year: Union[str, int] = date.today().year):
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
            Assertor.assert_data_types([age, income, year],
                                       [(str, int), (str, int, float), (int, str)])
            Assertor.assert_arguments([str(year)],
                                      [{'year': ('2018', '2019', '2020', '2021', '2022')}])

            self.age = str(age + 1)
            self.income = str(income)
            self.year = str(2022) if not year else str(year)
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
            .replace("skatteberegningsgrunnlagVersjon", self.tax_version_mapping[self.year][0]) \
            .replace("skattepliktVersjon", self.tax_version_mapping[self.year][1]) \
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
                    if any(key == "beregnetSkatt" + version for version in ['V2', 'V3', 'V4']):
                        for tag, val in value.items():
                            if tag == "skatteklasse":
                                tax_info.update({tag: val})
                            elif tag == "skatteregnskapskommune":
                                tax_info.update({tag: val})
                            elif tag == "informasjonTilSkattelister":
                                tax_info.update(
                                    {"nettoinntekt": Money(str(val["nettoinntekt"])).value()})
                                tax_info.update(
                                    {"nettoformue": Money(str(val["nettoformue"])).value()})
                                tax_info.update(
                                    {"beregnetSkatt": Money(str(val["beregnetSkatt"])).value()})
                            elif tag == "beregnetSkattFoerSkattefradrag":
                                tax_info.update(
                                    {tag: {"grunnlag": Money(str(val["grunnlag"])).value(),
                                           "beloep": Money(str(val["beloep"])).value()}})
                            elif tag == "beregnetSkatt":
                                tax_info.update(
                                    {tag: {"grunnlag": Money(str(val["grunnlag"])).value(),
                                           "beloep": Money(str(val["beloep"])).value()}})
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
                                            {sub_tag: {
                                                "grunnlag": Money(str(sub_val["grunnlag"])).value(),
                                                "beloep": Money(str(sub_val["beloep"])).value()}})
                    elif key == "beregningsgrunnlagV4":
                        for tag, val in value.items():
                            if tag == "beregningsgrunnlagsobjekt":
                                for element in val:
                                    tax_info.update(
                                        {element["tekniskNavn"]: Money(
                                            str(element["beloep"])).value()})
                    elif any(key == "summertSkattegrunnlagForVisning" + version for version in
                             ['V4', 'V5', 'V6', 'V7']):
                        for tag, val in value.items():
                            if tag == "skattegrunnlagsobjekt":
                                for element in val:
                                    tax_info.update(
                                        {element["tekniskNavn"]: Money(
                                            str(element["beloep"])).value()})
        return tax_info
