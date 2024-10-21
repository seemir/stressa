# -*- coding: utf-8 -*-
"""
Implementation of connector against Finn.no housing ad search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import json

import re
from time import time

from http.client import responses

import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from bs4 import BeautifulSoup

from source.util import LOGGER, TimeOutError, NoConnectionError, NotFoundError, \
    Assertor, Tracking

from source.app.connectors.settings import FINN_AD_URL, TIMEOUT
from source.app.connectors.finn import Finn


class FinnAd(Finn):
    """
    Connector that retrieves housing ad information from Finn.no given a Finn-code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        finn_code   : str
                      Finn-code to be search finn-ad information

        """
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(finn_code=finn_code)

    @Tracking
    def ad_response(self):
        """
        Response from Finn-no ad housing search

        Returns
        -------
        our     : requests.models.Response
                  response with housing ad information

        """
        try:
            try:
                start = time()
                ad_response = requests.get(
                    FINN_AD_URL + "{}".format(self.finn_code),
                    timeout=TIMEOUT)
                ad_status_code = ad_response.status_code
                if ad_status_code == 404:
                    ad_response = requests.get(
                        FINN_AD_URL.replace('homes',
                                            'newbuildings') + "{}".format(
                            self.finn_code),
                        timeout=TIMEOUT)
                    ad_status_code = ad_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    "HTTP status code -> ADVERT: [{}: {}] -> elapsed: {}".format(
                        ad_status_code, responses[ad_status_code], elapsed))
                return ad_response
            except ConnectTimeout as finn_ad_timeout_error:
                raise TimeOutError(
                    "Timeout occurred - please try again later or contact system "
                    "administrator, exited with '{}'".format(
                        finn_ad_timeout_error))
        except ConnectError as finn_ad_response_error:
            raise NoConnectionError(
                "Failed HTTP request - please insure that internet access is provided to the "
                "client or contact system administrator, exited with '{}'".format(
                    finn_ad_response_error))

    @Tracking
    def housing_ad_information(self):
        """
        Retrieve and parse housing ad information from Finn.no search to dict

        Returns
        -------
        out     : dict


        """
        try:
            LOGGER.info(
                "trying to retrieve 'housing_ad_information' for -> '{}'".format(
                    self.finn_code))
            response = self.ad_response()
            if not response:
                raise NotFoundError(
                    "[{}] Not found! '{}' may be an invalid Finn code".format(
                        self.__class__.__name__, self.finn_code))

            ad_soup = BeautifulSoup(response.content, "lxml")

            # with open('content.html', 'w', encoding='utf-8') as file:
            #     file.write(ad_soup.prettify())

            address = ad_soup.find("p", attrs={"class": "u-caption"})

            if not address:
                address = "".join(
                    set(value.text for value in
                        ad_soup.find_all("span", attrs={"class": "pl-4"}) if
                        "360° Visning" not in value.text)).replace("Video", "")
            else:
                address = address.text.replace("Video", "")

            price = "".join(
                price.text for price in
                ad_soup.find_all("span", attrs={"class": "u-t3"})
                if " kr" in price.text).strip().replace(u"\xa0", " ")

            if not price:
                price = "".join(
                    price.text for price in
                    ad_soup.find_all("span",
                                     attrs={"class": "text-28 font-bold"})
                    if " kr" in price.text).strip().replace(u"\xa0", " ")

            status = ad_soup.find("span",
                                  attrs={
                                      "class": "u-capitalize status status--warning u-mb0"})

            info = {"finn_adresse": address, "prisantydning": price,
                    "status": status.text.strip().replace(r'\n',
                                                          '').capitalize()
                    if status else "Ikke solgt"}

            keys, values = list(
                key.get_text() for key in ad_soup.find_all(["th", "dt"])), \
                list(value.get_text() for value in
                     ad_soup.find_all(["td", "dd"]))

            for key, val in zip(keys, values):
                key = re.sub("[^a-z]+", "", key.lower())
                val = val.strip().replace(u"\xa0", " ")
                if (key and len(key) > 3) or key == "rom":
                    info.update({key: val})

            visninger_days = []
            visninger_hours = []

            capitalize_first = "capitalize-first"

            for key in ad_soup.find_all("div",
                                        attrs={"class": capitalize_first}):
                if not key.get_text().capitalize() in visninger_days:
                    visninger_days.append(key.get_text().capitalize())

            font_bold_py_4 = 'font-bold py-4 mr-12'
            for key in ad_soup.find_all('div', attrs={"class": font_bold_py_4}):
                if not key.get_text() in visninger_hours:
                    visninger_hours.append(key.get_text())

            final_visninger = {"forste_visning": "", "andre_visning": ""}

            if visninger_days:
                if len(visninger_days) == 1:
                    final_visninger.update(
                        {"forste_visning": visninger_days[0] + ' kl. ' +
                                           visninger_hours[0]})
                else:
                    final_visninger.update(
                        {"forste_visning": visninger_days[0] + ' kl. ' +
                                           visninger_hours[0],
                         "andre_visning": visninger_days[1] + ' kl. ' +
                                          visninger_hours[1]})

            info.update(final_visninger)

            matrikkel = {}
            for key in ad_soup.find_all("p"):
                candidate = " ".join(key.get_text().split())
                if "Kommunenr:" in candidate and "Gårdsnr:" in candidate and \
                        "Bruksnr:" in candidate:
                    mat_list = candidate.split()
                    matrikkel.update(
                        {mat_list[i].replace(":", "").replace("å", "a")
                         .lower(): mat_list[i + 1] for i in
                         range(0, len(mat_list), 2)})
                if "-navn" in candidate and "-orgnummer" in candidate and \
                        "-andelsnummer" in candidate:
                    mat_list = [val.strip().split(":") for val in
                                key.get_text().split("\n") if val]
                    matrikkel.update(
                        {element[0].lower(): element[1].strip() for element in
                         mat_list})
                if "Seksjonsnr:" in candidate:
                    mat_list = candidate.split()
                    matrikkel.update(
                        {mat_list[i].replace(":", "").replace("å", "a")
                         .lower(): mat_list[i + 1] for i in
                         range(0, len(mat_list), 2)})

            if not matrikkel:
                for key in ad_soup.find_all("div"):
                    candidate = " ".join(key.get_text().split())

                    if "Kommunenr:" in candidate and all(
                            element not in candidate for element in
                            ['Gårdsnr:', 'Bruksnr:', 'Borettslag-navn:',
                             'Borettslag-orgnummer:',
                             'Borettslag-andelsnummer:']):
                        matrikkel.update({'kommunenr': str(
                            candidate.split(sep=':')[-1].strip())})
                    if "Gårdsnr:" in candidate and all(
                            element not in candidate for element in
                            ['Kommunenr:', 'Bruksnr:', 'Borettslag-navn:',
                             'Borettslag-orgnummer:',
                             'Borettslag-andelsnummer:']):
                        matrikkel.update({'gardsnr': str(
                            candidate.split(sep=':')[-1].strip())})
                    if "Bruksnr:" in candidate and all(
                            element not in candidate for element in
                            ['Kommunenr:', 'Gårdsnr:', 'Borettslag-navn:',
                             'Borettslag-orgnummer:',
                             'Borettslag-andelsnummer:']):
                        matrikkel.update({'bruksnr': str(
                            candidate.split(sep=':')[-1].strip())})
                    if "Borettslag-navn:" in candidate and all(
                            element not in candidate for element in
                            ['Kommunenr:', 'Gårdsnr:', 'Bruksnr:',
                             'Borettslag-orgnummer:',
                             'Borettslag-andelsnummer:']):
                        matrikkel.update(
                            {'borettslag-navn': str(
                                candidate.split(sep=':')[-1].strip())})
                    if "Borettslag-orgnummer:" in candidate and all(
                            element not in candidate for element in
                            ['Kommunenr:', 'Gårdsnr:', 'Bruksnr:',
                             'Borettslag-navn:',
                             'Borettslag-andelsnummer:']):
                        matrikkel.update(
                            {'borettslag-orgnummer': str(
                                candidate.split(sep=':')[-1].strip())})
                    if "Borettslag-andelsnummer:" in candidate and all(
                            element not in candidate for element in
                            ['Kommunenr:', 'Gårdsnr:', 'Bruksnr:',
                             'Borettslag-navn:',
                             'borettslag-orgnummer:']):
                        matrikkel.update(
                            {'borettslag-andelsnummer': str(
                                candidate.split(sep=':')[-1].strip())})
                    if "Seksjonsnr:" in candidate and all(
                            element not in candidate for element in
                            ['Kommunenr:', 'Gårdsnr:', 'Bruksnr:']):
                        matrikkel.update(
                            {'seksjonsnr': str(
                                candidate.split(sep=':')[-1].strip())})

            info.update({"matrikkel": matrikkel})

            script_tag = None

            for script in ad_soup.find_all('script'):
                if 'window.__remixContext' in script.text:
                    script_tag = script.text

            if script_tag:
                cleaned_script = (script_tag
                                  .replace(r'\u003e', '>')
                                  .replace(r'\u003c', '<')
                                  .replace(r'\u0026', '&')
                                  .replace('\n', ''))
                print(cleaned_script)

            LOGGER.success("'housing_ad_information' successfully retrieved")
            return info

        except AttributeError as no_housing_ad_information_exception:
            raise NotFoundError(
                "Not enough advert information found, exited with '{}'".format(
                    no_housing_ad_information_exception))

    @Tracking
    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save advert information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.housing_ad_information(), file_dir,
                       file_prefix="HousingAdInfo_")
        LOGGER.success(
            "'housing_ad_information' successfully parsed to JSON at '{}'".format(
                file_dir))


if __name__ == '__main__':
    finn_ad = FinnAd('371008605')

    finn_ad.housing_ad_information()
