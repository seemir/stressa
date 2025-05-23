# -*- coding: utf-8 -*-
"""
Module with logic for Skatteetaten Tax Info Connector

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking
from source.domain import TaxForm

from ...connectors import Skatteetaten, SKATTEETATEN_URL

from .operation import Operation


class SkatteetatenTaxInfoConnector(Operation):
    """
    Operation that retrieves Skatteetaten Tax info

    """

    _tax_value_mapping = {
        "alminneligInntektFoerFordelingsfradrag": "alminnelig_inntekt_foer_fordelingsfradrag",
        "alminneligInntektFoerSaerfradrag": "alminnelig_inntekt_foer_saerfradrag",
        "beregnetSkatt": "beregnet_skatt",
        "beregnetSkattFoerSkattefradrag": "beregnet_skatt_foer_skattefradrag",
        "bruttoformue": "bruttoformue",
        "ektefellenesSamledeVerdiFoerVerdsettingsrabattForAlleFormuesobjekter":
            "ektefellenes_samlede_verdi_foer_verdsettingsrabatt_for_alle_formuesobjekter",
        "fellesskatt": "fellesskatt",
        "formuesskattTilKommune": "formuesskatt_til_kommune",
        "formuesskattTilStat": "formuesskatt_til_stat",
        "formuesverdiForPrimaerbolig": "formuesverdi_for_primaerbolig",
        "formuesverdiSomPrimaerbolig": "formuesverdi_som_primaerbolig",
        "fradragForFagforeningskontingent": "fradrag_for_fagforeningskontingent",
        "gjeldIInnenlandskeBanker": "gjeld_i_innenlandske_banker",
        "innbetaltBeloepPaaBSUKontoIInntektsaar": "innbetalt_beloep_paa_bsu_konto_i_inntektsaar",
        "inntektsskattTilFylkeskommune": "inntektsskatt_til_fylkeskommune",
        "inntektsskattTilKommune": "inntektsskatt_til_kommune",
        "inntektsskattTilKommuneOgFylkeskommune": "inntektsskatt_til_kommune_og_fylkeskommune",
        "minstefradragIInntekt": "minstefradrag_i_inntekt",
        "nettoformue": "nettoformue",
        "nettoinntekt": "nettoinntekt",
        "personinntektFraLoennsinntekt": "personinntekt_fra_loennsinntekt",
        "samledeOpptjenteRenterIInnenlandskeBanker":
            "samlede_opptjente_renter_i_innenlandske_banker",
        "samledePaaloepteRenterPaaGjeldIInnenlandskeBanker":
            "samlede_paaloepte_renter_paa_gjeld_i_innenlandske_banker",
        "samletGjeld": "samlet_gjeld",
        "samletGrunnlagForInntektsskattTilKommuneOgFylkeskommuneStatsskattOgFellesskatt":
            "samlet_grunnlag_for_inntektsskatt_til_kommune_og_fylkeskommune_statsskatt_"
            "og_fellesskatt",
        "samletInnskuddIInnenlandskeBanker": "samlet_innskudd_i_innenlandske_banker",
        "samletLoennsinntektMedTrygdeavgiftspliktOgMedTrekkplikt":
            "samlet_loennsinntekt_med_trygdeavgiftsplikt_og_med_trekkplikt",
        "samletSkattepliktigOverskuddFraUtleieAvFastEiendom":
            "samlet_skattepliktig_overskudd_fra_utleie_av_fast_eiendom",
        "samletVerdiFoerVerdsettingsrabattForAlleFormuesobjekter":
            "samlet_verdi_foer_verdsettingsrabatt_for_alle_formuesobjekter",
        "samletVerdiFoerVerdsettingsrabattForPrimaerbolig":
            "samlet_verdi_foer_verdsettingsrabatt_for_primaerbolig",
        "skatteklasse": "skatteklasse",
        "skatteregnskapskommune": "skatteregnskapskommune",
        "sumFradragIAlminneligInntekt": "sum_fradrag_i_alminnelig_inntekt",
        "sumInntekterIAlminneligInntektFoerFordelingsfradrag":
            "sum_inntekter_i_alminnelig_inntekt_foer_fordelingsfradrag",
        "sumMinstefradrag": "sum_minstefradrag",
        "sumSkattefradrag": "sum_skattefradrag",
        "sumTrygdeavgift": "sum_trygdeavgift",
        "trinnskatt": "trinnskatt",
        "trygdeavgiftAvLoennsinntekt": "trygdeavgift_av_loennsinntekt"
    }

    @Tracking
    def __init__(self, tax_form: TaxForm):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        tax_form       : TaxForm
                         object with all tax input

        """
        Assertor.assert_data_types([tax_form], [TaxForm])
        super().__init__(name=self.__class__.__name__,
                         desc=f"from: '{SKATTEETATEN_URL}\\{tax_form.tax_year}' \n "
                              f"id: Skatteetaten Tax Info Connector")
        self.tax_form = tax_form

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : dict
                      dictionary with tax calculation

        """
        tax_info = Skatteetaten(age=self.tax_form.age,
                                income=self.tax_form.income,
                                tax_year=self.tax_form.tax_year,
                                interest_income=self.tax_form.interest_income,
                                interest_cost=self.tax_form.interest_cost,
                                value_of_real_estate=self.tax_form.value_of_real_estate,
                                bank_deposit=self.tax_form.bank_deposit,
                                debt=self.tax_form.debt,
                                union_fee=self.tax_form.union_fee,
                                bsu=self.tax_form.bsu,
                                other_income=self.tax_form.other_income,
                                rental_income=self.tax_form.rental_income)

        final_tax_info = {}
        for key, value in dict(sorted(tax_info.tax_information().items())).items():
            if key in self._tax_value_mapping:
                final_tax_info.update({self._tax_value_mapping[key]: value})
        return final_tax_info
