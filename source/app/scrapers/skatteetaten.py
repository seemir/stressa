# -*- coding: utf-8 -*-

"""
Implementation of scaper against Skatteetaten tax calculator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

# from source.util import Assertor, LOGGER, Tracking
#
# from .scraper import Scraper
#
#
# class Skatteetaten(Scraper):
#     """
#     Class that produces estimated total Taxes for a given year
#
#     """
#
#     def __init__(self, year: str, civil_status: str, year_of_birth: str, part_living: str,
#                  finnmark: str):
#         """
#         Constructor / Instantiate the class
#
#         Parameters
#         ----------
#
#
#         """
#         try:
#             super().__init__()
#             Assertor.assert_data_types([year, civil_status, year_of_birth, part_living, finnmark],
#                                        [str, str, str, str, str])
#             self.year = year
#             self.civil_status = year
#             self.year_of_birth = year_of_birth
#             self.part_living = part_living
#             self.finnmark = finnmark
#
#             LOGGER.success(
#                 "created '{}', with id: [{}]".format(self.__class__.__name__, self.id_))
#         except Exception as skatteetaten_exception:
#             LOGGER.exception(skatteetaten_exception)
#             raise skatteetaten_exception
#
# import json
#
# with open('skatteetaten_form.json') as json_file:
#     data = json.load(json_file)
#
# full_data = data["skatteberegningsgrunnlagV6"]["skattegrunnlagsobjekt"] + \
#             data["ektefelle"]["skatteberegningsgrunnlagV6"]["skattegrunnlagsobjekt"]
#
# tax_dict = []
#
# for elements in full_data:
#     element_dict = {}
#     for key, value in elements.items():
#         if key == "temakategori":
#             element_dict.update({key: value})
#         if key == "temaunderkategori":
#             element_dict.update({key: value})
#         if key == "postnummer":
#             element_dict.update({key: value})
#         if key == "ledetekst":
#             element_dict.update({key: value})
#         if key == "beloep":
#             element_dict.update({key: value})
#     tax_dict.append(element_dict)
#
# arbeidTrygdPensjon = 0
# bankLaanForsikring = 0
# boligOgEiendeler = 0
# familieOgHelse = 0
# finans = 0
# naering = 0
#
# for element in sorted(tax_dict, key=lambda i: i['temakategori']):
#     if element["temakategori"] == "arbeidTrygdPensjon":
#         arbeidTrygdPensjon += 1
#     if element["temakategori"] == "bankLaanForsikring":
#         bankLaanForsikring += 1
#     if element["temakategori"] == "boligOgEiendeler":
#         boligOgEiendeler += 1
#     if element["temakategori"] == "familieOgHelse":
#         familieOgHelse += 1
#     if element["temakategori"] == "finans":
#         finans += 1
#     if element["temakategori"] == "naering":
#         naering += 1
#
# print("arbeidTrygdPensjon ", arbeidTrygdPensjon)
# print("bankLaanForsikring ", bankLaanForsikring)
# print("boligOgEiendeler   ", boligOgEiendeler)
# print("familieOgHelse     ", familieOgHelse)
# print("finans             ", finans)
# print("naering            ", naering)
# print("total              ",
#       sum([arbeidTrygdPensjon, bankLaanForsikring, boligOgEiendeler, familieOgHelse, finans,
#            naering]))
