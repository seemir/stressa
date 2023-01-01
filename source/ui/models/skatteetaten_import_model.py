# -*- coding: utf-8 -*-
"""
Module containing TaxModel implementation

"""
__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from PyQt5.QtCore import QObject

from source.app import SkatteetatenTaxParsing
from source.util import Assertor

from .model import Model


class SkatteetatenImportModel(Model):
    """
    Model for Tax calculations and processing

    """
    _tax_output = ["beregnet_skatt_beloep", "beregnet_skatt_per_mnd_beloep",
                   "beregnet_skatt_foer_skattefradrag_beloep", "fellesskatt_grunnlag",
                   "fellesskatt_beloep", "fradrag_for_fagforeningskontingent", "gjeldsgrad",
                   "inntektsskatt_til_fylkeskommune_grunnlag",
                   "inntektsskatt_til_fylkeskommune_beloep", "inntektsskatt_til_kommune_grunnlag",
                   "inntektsskatt_til_kommune_beloep", "personinntekt_fra_loennsinntekt",
                   "samlet_gjeld", "samlede_paaloepte_renter_paa_gjeld_i_innenlandske_banker",
                   "samlede_opptjente_renter_i_innenlandske_banker",
                   "samlet_skattepliktig_overskudd_fra_utleie_av_fast_eiendom", "skatteklasse",
                   "skatteprosent", "skatteregnskapskommune", "sum_fradrag_i_alminnelig_inntekt",
                   "sum_inntekter_i_alminnelig_inntekt_foer_fordelingsfradrag", "sum_minstefradrag",
                   "sum_skattefradrag_beloep", "sum_trygdeavgift_grunnlag",
                   "sum_trygdeavgift_beloep", "trinnskatt_grunnlag", "trinnskatt_beloep"]

    def __init__(self, parent: QObject):
        """
        Constructor / Implementation

        """
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])

    @property
    def tax_output(self):
        """
        tax_output getter

        """
        return self._tax_output

    def import_tax_results(self, tax_results: dict):
        """
        method for calculate tax income

        """
        if tax_results:
            skatteetaten_parsing = SkatteetatenTaxParsing(tax_results)
            self.set_line_edits("", line_edits=self.tax_output,
                                data=skatteetaten_parsing.skatteetaten_results)
