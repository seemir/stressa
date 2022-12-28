# -*- coding: utf-8 -*-

"""
Module with logic of Flatten tax operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import Money

from .operation import Operation


class FlattenTaxResults(Operation):
    """
    Operation that flattens a tax dictionary

    """

    @Tracking
    def __init__(self, data: dict, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : dict
                      data to flatten
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([data, desc], [dict, str])
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with flatten data

        """
        parsed_dict = {}

        for item in self.data.keys():
            if item == "beregnetSkattFoerSkattefradrag":
                for key, value in self.data["beregnetSkattFoerSkattefradrag"].items():
                    if key == "grunnlag":
                        parsed_dict.update(
                            {"skatt_foer_skattefradrag_grunnlag": Money(str(value)).value()})
                    if key == "beloep":
                        parsed_dict.update(
                            {"beregnet_skatt_foer_skattefradrag_beloep": Money(str(value)).value()})
            if item == "beregnetSkatt":
                for key, value in self.data["beregnetSkatt"].items():
                    if key == "grunnlag":
                        parsed_dict.update({"beregnet_skatt_grunnlag": Money(str(value)).value()})
                    if key == "beloep":
                        parsed_dict.update({"beregnet_skatt_beloep": Money(str(value)).value()})
            if item == "skattOgAvgift":
                for keys, values in self.data["skattOgAvgift"].items():
                    # if keys == "formueskattTilStat":
                    #     for key, value in values.items():
                    #         if key == "grunnlag":
                    #             parsed_dict.update(
                    #                 {"formuesskatt_til_stat_grunnlag": Money(str(value)).value()})
                    #         if key == "beloep":
                    #             parsed_dict.update(
                    #                 {"formuesskatt_til_stat_beloep": Money(str(value)).value()})
                    if keys == "inntektsskattTilKommune":
                        for key, value in values.items():
                            if key == "grunnlag":
                                parsed_dict.update(
                                    {"inntektsskatt_til_kommune_grunnlag": Money(
                                        str(value)).value()})
                            if key == "beloep":
                                parsed_dict.update(
                                    {"inntektsskatt_til_kommune_beloep": Money(str(value)).value()})
                    if keys == "inntektsskattTilFylkeskommune":
                        for key, value in values.items():
                            if key == "grunnlag":
                                parsed_dict.update(
                                    {"inntektsskatt_til_fylkeskommune_grunnlag": Money(
                                        str(value)).value()})
                            if key == "beloep":
                                parsed_dict.update(
                                    {"inntektsskatt_til_fylkeskommune_beloep": Money(
                                        str(value)).value()})
                    # if keys == "formueskattTilKommune":
                    #     for key, value in values.items():
                    #         if key == "grunnlag":
                    #             parsed_dict.update(
                    #                 {"formuesskatt_til_kommune_grunnlag": Money(
                    #                     str(value)).value()})
                    #         if key == "beloep":
                    #             parsed_dict.update(
                    #                 {"formuesskatt_til_kommune_beloep": Money(
                    #                     str(value)).value()})
                    if keys == "fellesskatt":
                        for key, value in values.items():
                            if key == "grunnlag":
                                parsed_dict.update(
                                    {"fellesskatt_grunnlag": Money(
                                        str(value)).value()})
                            if key == "beloep":
                                parsed_dict.update(
                                    {"fellesskatt_beloep": Money(
                                        str(value)).value()})
                    if keys == "trinnskatt":
                        for key, value in values.items():
                            if key == "grunnlag":
                                parsed_dict.update(
                                    {"trinnskatt_grunnlag": Money(
                                        str(value)).value()})
                            if key == "beloep":
                                parsed_dict.update(
                                    {"trinnskatt_beloep": Money(
                                        str(value)).value()})
                    if keys == "sumTrygdeavgift":
                        for key, value in values.items():
                            if key == "grunnlag":
                                parsed_dict.update(
                                    {"sum_trygdeavgift_grunnlag": Money(
                                        str(value)).value()})
                            if key == "beloep":
                                parsed_dict.update(
                                    {"sum_trygdeavgift_beloep": Money(
                                        str(value)).value()})
        return parsed_dict
