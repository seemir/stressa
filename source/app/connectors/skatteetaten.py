# -*- coding: utf-8 -*-

"""
Implementation of connector against Skatteetaten tax calculator

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

from source.util import Assertor, LOGGER, NoConnectionError, TimeOutError, \
    Tracking
from source.domain import Money

from .settings import SKATTEETATEN_URL, TIMEOUT
from .connector import Connector


class Skatteetaten(Connector):  # pylint: disable=too-many-instance-attributes
    """
    Class that produces estimated total Taxes for a given year

    """

    tax_version_mapping = {
        '2023': ('skatteberegningsgrunnlag', 'skatteplikt'),
        '2022': ('skatteberegningsgrunnlagV7', 'skattepliktV9'),
        '2021': ('skatteberegningsgrunnlagV6', 'skattepliktV8'),
        '2020': ('skattegrunnlagV6', 'skattepliktV7'),
        '2019': ('skattegrunnlagV5', 'skattepliktV6'),
        '2018': ('skattegrunnlagV5', 'skattepliktV5')
    }

    def __init__(self, age: Union[str, int],
                 income: Union[str, int, float],
                 tax_year: Union[str, int] = date.today().year,
                 interest_income: Union[str, int, float] = 0,
                 interest_cost: Union[str, int, float] = 0,
                 value_of_real_estate: Union[str, int, float] = 0,
                 bank_deposit: Union[str, int, float] = 0,
                 debt: Union[str, int, float] = 0,
                 union_fee: Union[str, int, float] = 0,
                 bsu: Union[str, int, float] = 0,
                 other_income: Union[str, int, float] = 0,
                 rental_income: Union[str, int, float] = 0):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        age                 : str, int
                              age of individual
        income              : str, int, float
                              income of individual
        tax_year            : str, int
                              tax year to calculate taxes
        interest_income     : str, int, float
                              income of interest
        interest_cost       : str, int, float
                              cost of income
        value_of_real_estate: str, int, float
                              value of real-estate (if any applies)
        bank_deposit        : str, int, float
                              value of bank deposit
        debt                : str, int, float
                              total debt
        union_fee           : str, int, float
                              yearly union fee
        bsu                 : str, int, float
                              yearly bsu savings
        other_income        : str, int, float
                              other income to be taxed
        rental_income       : str, int, float
                              rental income

        """

        try:
            super().__init__()
            Assertor.assert_data_types(
                [age, income, tax_year, interest_income, interest_cost,
                 value_of_real_estate, bank_deposit, debt, union_fee, bsu,
                 other_income, rental_income],
                [(str, int), (str, int, float), (int, str),
                 (int, str, float), (int, str, float),
                 (int, str, float), (int, str, float),
                 (int, str, float), (int, str, float),
                 (int, str, float), (int, str, float),
                 (int, str, float)])
            Assertor.assert_arguments([str(tax_year)],
                                      [{'year': (
                                          '2018', '2019', '2020', '2021',
                                          '2022', '2023')}])

            self.age = str(age)
            self.income = str(income)
            self.tax_year = str(date.today().year) if not tax_year else str(
                tax_year)
            self.interest_income = str(0) if not interest_income else str(
                interest_income)
            self.interest_cost = str(0) if not interest_cost else str(
                interest_cost)
            self.value_of_real_estate = str(
                0) if not value_of_real_estate else str(
                value_of_real_estate)
            self.bank_deposit = str(0) if not bank_deposit else str(
                bank_deposit)
            self.debt = str(0) if not debt else str(debt)
            self.union_fee = str(0) if not union_fee else str(union_fee)
            self.bsu = str(0) if not bsu else str(bsu)
            self.other_income = str(0) if not other_income else str(
                other_income)
            self.rental_income = str(0) if not rental_income else str(
                rental_income)
            self.url = f"{SKATTEETATEN_URL}{self.tax_year}"

            LOGGER.success(
                f"created '{self.__class__.__name__}', with id: [{self.id_}]")
        except Exception as skatteetaten_exception:
            LOGGER.exception(skatteetaten_exception)
            raise skatteetaten_exception

    @Tracking
    def payload(self):
        """
        method for generating payload str

        """
        with open(os.path.dirname(
                __file__) + '\\payloads\\skatteetaten_payload.json',
                  encoding='utf-8') as json_file:
            json_data = json.load(json_file)
        tax_payload = json.dumps(json_data) \
            .replace("alderIInntektsaarVerdi", self.age) \
            .replace("loennsinntektNaturalytelseMvBelop", self.income) \
            .replace("skatteberegningsgrunnlagVersjon",
                     self.tax_version_mapping[self.tax_year][0]) \
            .replace("skattepliktVersjon",
                     self.tax_version_mapping[self.tax_year][1]) \
            .replace("opptjenteRenterBelop", self.interest_income) \
            .replace("paaloepteRenterBelop", self.interest_cost) \
            .replace("formuesverdiForPrimaerboligBelop",
                     self.value_of_real_estate) \
            .replace("innskuddBelop", self.bank_deposit) \
            .replace("gjeldBelop", self.debt) \
            .replace("betaltFagforeningskontingentBelop", self.union_fee) \
            .replace("beloepSpartIBSUIInntektsaarBelop", self.bsu) \
            .replace("annenArbeidsinntektBeloep", self.other_income) \
            .replace("nettoinntektVedUtleieAvFastEiendomMvBeloep",
                     self.rental_income)

        if self.tax_year == "2023":

            tax_payload = json.loads(tax_payload)
            tax_base_object = []

            value_of_home = 0
            bsu_value = 0

            for tax_element in tax_payload['skatteberegningsgrunnlag']['skattegrunnlagsobjekt']:
                tax_element_dict = {}

                technical_name = tax_element['tekniskNavn']
                amount = tax_element['beloep']

                if technical_name == 'formuesverdiForPrimaerbolig':
                    value_of_home = amount
                    tax_element_dict.update({'tekniskNavn': technical_name, 'beloep': int(amount),
                                             "verdiFoerVerdsettingsrabattForFastEiendom": int(int(
                                                 amount) / 0.25)})
                elif technical_name == 'inntektsfradragForFagforeningskontingent':
                    tax_element_dict.update({'tekniskNavn': technical_name, 'beloep': int(amount)})
                elif technical_name == 'beloepSpartIBSUIInntektsaar':
                    bsu_value = amount
                    tax_element_dict.update({'tekniskNavn': technical_name, 'beloep': amount})
                else:
                    tax_element_dict.update({'tekniskNavn': technical_name, 'beloep': amount})

                tax_base_object.append(tax_element_dict)

            if value_of_home == 0 and bsu_value == 0:
                for element in tax_base_object:
                    if element['tekniskNavn'] in ['formuesverdiForPrimaerbolig',
                                                  'beloepSpartIBSUIInntektsaar']:
                        tax_base_object.remove(element)
            elif (value_of_home != 0 and bsu_value != 0) or (value_of_home != 0 and bsu_value == 0):
                for element in tax_base_object:
                    if element['tekniskNavn'] == 'beloepSpartIBSUIInntektsaar':
                        tax_base_object.remove(element)
            elif value_of_home == 0 and bsu_value != 0:
                for element in tax_base_object:
                    if element['tekniskNavn'] == 'formuesverdiForPrimaerbolig':
                        tax_base_object.remove(element)

            tax_payload['skatteberegningsgrunnlag'].update(
                {'skattegrunnlagsobjekt': tax_base_object})

            tax_payload = json.dumps(tax_payload)
            tax_payload = tax_payload.replace('skattegrunnlagsobjekt',
                                              'skatteberegningsgrunnlagsobjekt')
        return tax_payload

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
                response = requests.post(url=self.url, data=self.payload(),
                                         timeout=TIMEOUT)
                status_code = response.status_code
                LOGGER.info(
                    f"HTTP status code -> [{status_code}: {responses[status_code]}]")
                return response
            except ConnectTimeout as ssb_timeout_error:
                raise TimeOutError(
                    f"Timeout occurred - please try again later or contact system administrator, "
                    f"exited with '{ssb_timeout_error}'")
        except ConnectError as ssb_response_error:
            raise NoConnectionError(
                f"Failed HTTP request - please ensure that internet access is provided to the "
                f"client or contact system administrator, exited with '{ssb_response_error}'")

    @Tracking
    def tax_information(self):
        """
        method for getting tax dict given information passed to class

        Returns
        -------
        out     : dict
                  tax information given information passed through class

        """

        try:
            tax_dict = self.response().json()
            tax_info = {}

            for keys, values in tax_dict.items():
                if keys == "hovedperson":
                    for key, value in values.items():
                        if any(key == "beregnetSkatt" + version for version in
                               ['V2', 'V3', 'V4', '']):
                            for tag, val in value.items():
                                if tag == "skatteklasse":
                                    tax_info.update({tag: val})
                                elif tag == "skatteregnskapskommune":
                                    tax_info.update({tag: val})
                                elif tag == "informasjonTilSkattelister":
                                    tax_info.update(
                                        {"nettoinntekt": Money(
                                            str(val["nettoinntekt"])).value()})
                                    tax_info.update(
                                        {"nettoformue": Money(
                                            str(val["nettoformue"])).value()})
                                    tax_info.update(
                                        {"beregnetSkatt": Money(
                                            str(val["beregnetSkatt"])).value()})
                                elif tag in ["beregnetSkattFoerSkattefradrag",
                                             "sumSkattefradrag",
                                             "beregnetSkatt"]:
                                    if isinstance(val, dict):
                                        tax_info.update(
                                            {tag: {"grunnlag": Money(
                                                str(val["grunnlag"])).value(),
                                                   "beloep": Money(
                                                       str(val["beloep"])).value()}})
                                    else:
                                        tax_info.update({tag: {"grunnlag": '',
                                                               "beloep": Money(
                                                                   str(val)).value()}})
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
                                                    "grunnlag": Money(str(sub_val[
                                                                              "grunnlag"])).value(),
                                                    "beloep": Money(str(sub_val[
                                                                            "beloep"])).value()}})
                        elif key == "beregningsgrunnlagV4":
                            for tag, val in value.items():
                                if tag == "beregningsgrunnlagsobjekt":
                                    for element in val:
                                        tax_info.update(
                                            {element["tekniskNavn"]: Money(
                                                str(element["beloep"])).value()})
                        elif any(key == "summertSkattegrunnlagForVisning" + version
                                 for version in
                                 ['V4', 'V5', 'V6', 'V7', '']):
                            for tag, val in value.items():
                                if tag in ["skattegrunnlagsobjekt",
                                           "skatteberegningsgrunnlagsobjekt"]:
                                    for element in val:
                                        if element[
                                            'tekniskNavn'] == 'nettoinntektVedUtleieAvFastEiendomMv':
                                            tax_info.update(
                                                {
                                                    "samletSkattepliktigOverskuddFraUtleieAvFastEiendom": Money(
                                                        str(element["beloep"])).value()})
                                        elif element[
                                            'tekniskNavn'] == 'samletLoennsinntektMedTrygdeavgiftspliktOgMedTrekkplikt':
                                            tax_info.update(
                                                {
                                                    "personinntektFraLoennsinntekt": Money(
                                                        str(element["beloep"])).value()})
                                        else:
                                            tax_info.update(
                                                {element["tekniskNavn"]: Money(
                                                    str(element["beloep"])).value()})
            return tax_info
        except Exception as skatteetaten_exception:
            error_msg = f"skatteetaten error, exited with '{str(skatteetaten_exception)}'"
            LOGGER.exception(error_msg)
            raise skatteetaten_exception
