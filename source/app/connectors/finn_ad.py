# -*- coding: utf-8 -*-
"""
Implementation of connector against Finn.no housing ad search

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from time import time
from datetime import datetime
from http.client import responses

import pytz
import requests
from requests.exceptions import ConnectTimeout, ConnectionError as ConnectError

from bs4 import BeautifulSoup

import json_repair

from source.util import LOGGER, TimeOutError, NoConnectionError, \
    InvalidDataError, Assertor, Tracking
from source.domain import Money, Amount

from .settings import FINN_AD_URL, TIMEOUT
from .finn import Finn


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
                    FINN_AD_URL + f"{self.finn_code}",
                    timeout=TIMEOUT)
                ad_status_code = ad_response.status_code
                elapsed = self.elapsed_time(start)
                LOGGER.info(
                    f"HTTP status code -> ADVERT: [{ad_status_code}: {responses[ad_status_code]} "
                    f"-> elapsed: {elapsed}")
                return ad_response
            except ConnectTimeout as finn_ad_timeout_error:
                raise TimeOutError(
                    f"Timeout occurred - please try again later or contact system administrator, "
                    f"exited with '{finn_ad_timeout_error}'")
        except ConnectError as finn_ad_response_error:
            raise NoConnectionError(
                f"Failed HTTP request - please insure that internet access is provided to the "
                f"client or contact system administrator, exited with '{finn_ad_response_error}'")

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
                f"trying to retrieve 'housing_ad_information' for -> '{self.finn_code}'")
            response = self.ad_response()
            if not response:
                raise InvalidDataError(
                    f"[{self.__class__.__name__}] Not found! '{self.finn_code}' "
                    f"may be an invalid Finn code")

            ad_soup = BeautifulSoup(response.content, "lxml")

            info = {}
            ad_data = None
            meta_data = None
            script_tag = None

            for script in ad_soup.find_all('script'):
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
                        if 'routes/realestate+/_item+/homes.ad[.html]' in loader_data:
                            routes = loader_data[
                                'routes/realestate+/_item+/homes.ad[.html]']
                            if 'objectData' in routes:
                                object_data = routes['objectData']
                                if 'ad' in object_data:
                                    ad_data = object_data['ad']
                                if 'meta' in object_data:
                                    meta_data = object_data['meta']

            if ad_data:

                street_address = ''
                postal_code = ''
                postal_place = ''
                floor = ''
                collective_debt = ''
                collective_assets = ''
                municipal_fees = ''
                shared_cost = ''
                advertiser_ref = ''
                energy_label = ''
                first_viewing = ''
                second_viewing = ''
                tax_value = ''
                plot_area = ''
                usable_size = ''
                usable_area_i = ''
                usable_area_e = ''
                total_price = ''
                sales_cost_sum = ''
                ad_history = {}

                matrikkel = {'kommunenr': '',
                             'gardsnr': '',
                             'bruksnr': '',
                             'bruksenhetsnr': '',
                             'borettslag-andelsnummer': '',
                             'borettslag-navn': '',
                             'borettslag-orgnummer': ''}

                if 'streetAddress' in ad_data['location']:
                    street_address = ad_data['location']['streetAddress']
                if 'postalCode' in ad_data['location']:
                    postal_code = ad_data['location']['postalCode']
                if 'postalPlace' in ad_data['location']:
                    postal_place = ad_data['location']['postalPlace']

                status = 'Solgt' if ad_data['disposed'] else 'Ikke solgt'
                address = f'{street_address}, {postal_code} {postal_place}'
                price = Money(str(ad_data['price']['suggestion'])).value()

                if 'total' in ad_data['price']:
                    total_price = Money(str(ad_data['price']['total'])).value()
                if 'salesCostSum' in ad_data['price']:
                    sales_cost_sum = Money(
                        str(ad_data['price']['salesCostSum'])).value()
                if 'collectiveDebt' in ad_data['price']:
                    collective_debt = Money(
                        str(ad_data['price']['collectiveDebt'])).value()
                if 'collectiveAssets' in ad_data['price']:
                    collective_assets = Money(
                        str(ad_data['price']['collectiveAssets'])).value()
                if 'municipalFees' in ad_data['price']:
                    municipal_fees = Money(
                        str(ad_data['price']['municipalFees'])).value()
                if 'taxValue' in ad_data['price']:
                    tax_value = Money(str(ad_data['price']['taxValue'])).value()

                if 'usable' in ad_data['size']:
                    usable_size = Amount(
                        str(ad_data['size']['usable'])).amount + ' m²'
                if 'usableAreaI' in ad_data['size']:
                    usable_area_i = Amount(
                        str(ad_data['size'][
                                'usableAreaI'])).amount + ' m² (BRA-i)'
                if 'usableAreaE' in ad_data['size']:
                    usable_area_e = Amount(
                        str(ad_data['size'][
                                'usableAreaE'])).amount + ' m² (BRA-e)'

                bedrooms = Amount(str(ad_data['bedrooms'])).amount
                property_type = ad_data['propertyType']
                ownership_type = ad_data['ownershipType']

                if 'floor' in ad_data:
                    floor = Amount(str(ad_data['floor'])).amount

                if 'area' in ad_data['plot']:
                    plot_area = Amount(str(ad_data['plot']['area'])).amount

                owned_plot = ad_data['plot']['owned']
                construction_year = str(ad_data['constructionYear'])
                viewings = ad_data['viewings']

                if 'sharedCost' in ad_data:
                    shared_cost = Money(
                        str(ad_data['sharedCost']['amount'])).value()

                if len(viewings) == 1:
                    if 'dateIso' in viewings[0]:
                        first_viewing = \
                            f"{self._convert_isodate_to_local(viewings[0]['dateIso'])} " \
                            f"kl. {viewings[0]['from']}-{viewings[0]['to']}"
                if len(viewings) >= 2:

                    if 'dateIso' in viewings[0]:
                        first_viewing = \
                            f"{self._convert_isodate_to_local(viewings[0]['dateIso'])} " \
                            f"kl. {viewings[0]['from']}-{viewings[0]['to']}"

                    if 'dateIso' in viewings[1]:
                        second_viewing = \
                            f"{self._convert_isodate_to_local(viewings[1]['dateIso'])} " \
                            f"kl. {viewings[1]['from']}-{viewings[1]['to']}"

                cadastres = ad_data['cadastres']

                if cadastres:
                    if 'municipalityNumber' in cadastres[0]:
                        matrikkel.update(
                            {'kommunenr': str(
                                cadastres[0]['municipalityNumber'])})
                    if 'landNumber' in cadastres[0]:
                        matrikkel.update(
                            {'gardsnr': str(cadastres[0]['landNumber'])})
                    if 'titleNumber' in cadastres[0]:
                        matrikkel.update(
                            {'bruksnr': str(cadastres[0]['titleNumber'])})
                    if 'partOwnershipNumber' in cadastres[0]:
                        matrikkel.update(
                            {'borettslag-andelsnummer': str(
                                cadastres[0]['partOwnershipNumber'])})
                    if 'apartmentNumber' in cadastres[0]:
                        matrikkel.update(
                            {'bruksenhetsnr': str(
                                cadastres[0]['apartmentNumber'])})
                    if 'sectionNumber' in cadastres[0]:
                        matrikkel.update(
                            {'seksjonsnr': str(
                                cadastres[0]['sectionNumber'])})

                if 'housingCooperative' in ad_data:
                    matrikkel.update({'borettslag-navn':
                                          ad_data['housingCooperative'][
                                              'name']})
                    matrikkel.update({'borettslag-orgnummer':
                                          ad_data['housingCooperative'][
                                              'organisationNumber']})

                edited = self._convert_isodate_to_local(meta_data['edited'])
                published = self._convert_isodate_to_local(
                    meta_data['history'][0]['broadcasted'],
                    norwegian_format=True)
                first_published = self._convert_isodate_to_local(
                    meta_data['history'][0]['broadcasted'], days_delta=True,
                    include_time=False)

                if 'history' in meta_data:
                    ad_history = meta_data['history']
                    mode = []
                    version = []
                    broadcasted = []

                    for history in ad_history:
                        mode.append(history['mode'])
                        version.append(history['version'])
                        broadcasted.append(
                            self._convert_isodate_to_local(
                                history['broadcasted'], days_delta=True))

                    ad_history = {'Versjon': version, 'Modus': mode,
                                  'Oppdatert': broadcasted}

                if 'advertiserRef' in ad_data:
                    advertiser_ref = ad_data['advertiserRef']
                elif 'externalAdId' in ad_data:
                    advertiser_ref = ad_data['externalAdId']

                if 'energyLabel' in ad_data:
                    color_scale = {
                        "DARK_GREEN": "Mørkegrønn",
                        "LIGHT_GREEN": "Lysegrønn",
                        "YELLOW": "Gul",
                        "ORANGE": "Oransje",
                        "RED": "Rød"
                    }
                    energy_label_class = ad_data['energyLabel']['class']
                    energy_label_color = ad_data['energyLabel']['color']
                    energy_label = f"{energy_label_class} - {color_scale[energy_label_color]}"
                if 'changeOfOwnershipInsurance' in ad_data:
                    change_of_ownership_insurance = ad_data[
                        'changeOfOwnershipInsurance']
                    if change_of_ownership_insurance:
                        change_of_ownership_insurance = 'Ja'
                    else:
                        change_of_ownership_insurance = 'Nei'
                else:
                    change_of_ownership_insurance = 'Nei'

                images = ad_data['images']

                info.update({'finnkode': self.finn_code,
                             'status': status,
                             'finn_adresse': address,
                             'images': images,
                             'prisantydning': price,
                             'totalpris': total_price,
                             'omkostninger': sales_cost_sum,
                             'felleskostmnd': shared_cost,
                             'fellesgjeld': collective_debt,
                             'fellesformue': collective_assets,
                             'bruksareal': usable_size,
                             'eksterntbruksareal': usable_area_e,
                             'interntbruksareal': usable_area_i,
                             'soverom': bedrooms,
                             'boligtype': property_type,
                             'eieform': ownership_type,
                             'etasje': floor,
                             'tomteareal': plot_area + f" m² ({'eiet' if owned_plot else 'festet'})"
                             if plot_area else '',
                             'bygger': construction_year,
                             'forste_visning': first_viewing.capitalize(),
                             'andre_visning': second_viewing.capitalize(),
                             'sistendret': edited,
                             'published': published,
                             'firstpublished': first_published,
                             'referanse': advertiser_ref,
                             'energimerking': energy_label,
                             'kommunaleavg': municipal_fees,
                             'formuesverdi': tax_value,
                             'boligselgerforsikring': change_of_ownership_insurance,
                             'annonse_historikk': ad_history})

                for key, value in matrikkel.items():
                    info.update({key: value})

                LOGGER.success(
                    "'housing_ad_information' successfully retrieved")

                return info
            raise ValueError('No ad info found')

        except Exception as invalid_data_exception:
            raise InvalidDataError(
                f"Something went wrong, exited with '{invalid_data_exception}'")

    @staticmethod
    def _convert_isodate_to_local(isodate: str, days_delta: bool = False,
                                  include_time: bool = True,
                                  norwegian_format: bool = False):
        """
        helper method for converting iso date to Norwegin date format

        Parameters
        ----------
        isodate           : str
                            isodate to be formatted
        days_delta        : bool
                            flag for delta days
        include_time      : bool
                            flag for including time
        norwegian_format  : bool
                            flag if one wants norwegian dateformat

        Returns
        -------
        out               : str
                            formatted isodate

        """

        norwegian_weekdays = ["man", "tir", "ons", "tor",
                              "fre", "lør", "søn"]
        norwegian_months = ["jan", "feb", "mar", "apr", "mai", "jun",
                            "jul", "aug", "sep", "okt",
                            "nov", "des"]
        if 'T' in isodate:
            try:
                utc_time = datetime.fromisoformat(isodate)
            except ValueError:
                date_part, time_part = isodate.split('T')
                time_part = time_part.split('+')[0]
                if '.' in time_part:
                    time_part = time_part.split('.')
                    time_part[1] = time_part[1][:3]
                    time_part = '.'.join(time_part)

                corrected_iso_string = f"{date_part}T{time_part}+02:00"  # Add back the timezone
                utc_time = datetime.fromisoformat(corrected_iso_string)

            cet_timezone = pytz.timezone("Europe/Berlin")
            date_obj = utc_time.astimezone(cet_timezone)
        else:
            date_obj = datetime.strptime(isodate, "%Y-%m-%d")

        if norwegian_format:
            return date_obj.strftime("%d.%m.%Y %H:%M")

        weekday = norwegian_weekdays[date_obj.weekday()]
        month = norwegian_months[date_obj.month - 1]
        formatted_date = f"{weekday.capitalize()}, {date_obj.day}. {month} {date_obj.year}"

        if 'T' in isodate and include_time:
            formatted_date = formatted_date + f" kl.{date_obj.hour:02}:{date_obj.minute:02}"

        if days_delta:
            delta = datetime.today().replace(tzinfo=None) - date_obj.replace(
                tzinfo=None)
            formatted_date = formatted_date + f" ({delta.days} dager)"

        return formatted_date

    @Tracking
    def to_json(self, file_dir: str = "report/json/finn_information"):
        """
        save advert information to JSON file

        """
        Assertor.assert_data_types([file_dir], [str])
        self.save_json(self.housing_ad_information(), file_dir,
                       file_prefix="HousingAdInfo_")
        LOGGER.success(
            f"'housing_ad_information' successfully parsed to JSON at '{file_dir}'")
