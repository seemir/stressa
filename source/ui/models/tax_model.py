# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from decimal import Decimal

from PyQt5.QtCore import QObject

from source.app import SkatteetatenTaxProcessing
from source.util import Assertor
from source.domain import Money

from .model import Model


class TaxModel(Model):
    _tax_year = ["", "2022", "2021", "2020", "2019", "2018"]
    _total_posts = ["brutto_inntekt_total", "trygde_inntekt_total", "leieinntekt_total",
                    "renteinntekter_total", "andre_inntekter_total", "personinntekt_total",
                    "rentekostnader_total"]
    _tax_input = ["skatte_aar", "alder", "fagforeningskontigent", "bsu", "rentekostnader_total",
                  "verdi_primarbolig", "bankinnskudd", "gjeld"]
    _tax_output = ["beregnet_skatt_grunnlag", "beregnet_skatt_beloep",
                   "beregnet_skatt_foer_skattefradrag_grunnlag", "beregnet_skatt_per_mnd_beloep",
                   "beregnet_skatt_foer_skattefradrag_beloep", "fellesskatt_grunnlag",
                   "fellesskatt_beloep", "formuesskatt_til_kommune_grunnlag",
                   "formuesskatt_til_kommune_beloep", "formuesskatt_til_stat_grunnlag",
                   "formuesskatt_til_stat_beloep", "fradrag_for_fagforeningskontingent",
                   "gjeldsgrad", "inntektsskatt_til_fylkeskommune_grunnlag",
                   "inntektsskatt_til_fylkeskommune_beloep", "inntektsskatt_til_kommune_grunnlag",
                   "inntektsskatt_til_kommune_beloep", "personinntekt_fra_loennsinntekt",
                   "samlet_gjeld", "samlede_paaloepte_renter_paa_gjeld_i_innenlandske_banker",
                   "samlede_opptjente_renter_i_innenlandske_banker",
                   "samlet_skattepliktig_overskudd_fra_utleie_av_fast_eiendom", "skatteklasse",
                   "skatteprosent", "skatteregnskapskommune", "sum_fradrag_i_alminnelig_inntekt",
                   "sum_inntekter_i_alminnelig_inntekt_foer_fordelingsfradrag", "sum_minstefradrag",
                   "sum_skattefradrag_grunnlag", "sum_skattefradrag_beloep",
                   "sum_trygdeavgift_grunnlag", "sum_trygdeavgift_beloep",
                   "trinnskatt_grunnlag", "trinnskatt_beloep"]

    def __init__(self, parent: QObject):
        super().__init__(parent)
        Assertor.assert_data_types([parent], [QObject])

        self.parent.ui.combo_box_skatte_aar.addItems(self.tax_year)

    @property
    def tax_year(self):
        return self._tax_year

    @property
    def total_posts(self):
        return self._total_posts

    @property
    def tax_input(self):
        return self._tax_input

    @property
    def tax_output(self):
        return self._tax_output

    def tax_info(self):
        self.parent.ui.combo_box_skatte_aar.activated.connect(
            lambda: self.set_combo_box("skatte_aar", key_name="skatte_aar"))
        self.parent.ui.line_edit_alder.textEdited.connect(
            lambda: self.set_line_edit("alder"))

        self.parent.ui.line_edit_fagforeningskontigent.textEdited.connect(
            lambda: self.set_value('fagforeningskontigent'))
        self.parent.ui.line_edit_bsu.textEdited.connect(
            lambda: self.set_value('bsu'))
        self.parent.ui.line_edit_verdi_primarbolig.textEdited.connect(
            lambda: self.set_value('verdi_primarbolig'))
        self.parent.ui.line_edit_bankinnskudd.textEdited.connect(
            lambda: self.set_value('bankinnskudd'))
        self.parent.ui.line_edit_gjeld.textEdited.connect(
            lambda: self.set_value('gjeld'))
        self.parent.ui.line_edit_netto_formue.textEdited.connect(
            lambda: self.set_value('netto_formue'))
        self.set_line_edits("", line_edits=self.total_posts,
                            data=self.parent.parent.budget_view.budget_model.data)

    def set_value(self, line_edit):
        if getattr(self.parent.ui, "line_edit_" + line_edit).text():
            self.set_line_edit(line_edit, Money, "value")
        else:
            self.clear_line_edit(line_edit)
        self.net_wealth()

    def net_wealth(self):
        verdi_bolig = self.parent.ui.line_edit_verdi_primarbolig.text()
        bankinnskudd = self.parent.ui.line_edit_bankinnskudd.text()
        gjeld = self.parent.ui.line_edit_gjeld.text()
        net_wealth = self.calculate_net_wealth("netto_formue", verdi_bolig, bankinnskudd, gjeld)
        if net_wealth != "0" or not net_wealth:
            self.set_line_edit("netto_formue", data=Money(str(net_wealth)).value())
        else:
            self.clear_line_edit("netto_formue")

    def calculate_net_wealth(self, line_edit: str, real_estate: str, bank_deposit: str, debt: str):
        net_wealth = (Decimal(real_estate.replace(" ", "").replace("kr", "")) if real_estate else
                      Decimal("0")) + (
                         Decimal(bank_deposit.replace(" ", "").replace("kr", "")) if bank_deposit
                         else Decimal("0")) - (
                         Decimal(debt.replace(" ", "").replace("kr", "")) if debt else
                         Decimal("0"))
        self.data.update({line_edit: Money(str(net_wealth)).value()})
        return str(net_wealth)

    def calculate_tax_income(self):
        if "brutto_inntekt_total" in self.data.keys() and "skatte_aar" in self.data.keys() and \
                "alder" in self.data.keys():
            self.clear_line_edits(self.tax_output)
            self.parent.ui.tab_widget_skattekalkulator.setCurrentIndex(1)
            tax_form = {key: val.replace(" ", "").replace("kr", "") for key, val in
                        self.data.items() if key in self.tax_input}
            brutto_inntekt = Money(self.data["brutto_inntekt_total"]) * Money("12")

            if "trygde_inntekt_total" in self.data.keys():
                trygd = Money(self.data["trygde_inntekt_total"]) * Money("12")
            else:
                trygd = "0"

            total_sub_income = Money(brutto_inntekt) + Money(trygd)

            tax_form.update({'inntekt_total': total_sub_income.replace(" ", "").replace("kr", "")})

            if 'renteinntekter_total' in self.data.keys():
                tax_form.update({'renteinntekter_total': (
                        Money(self.data["renteinntekter_total"]) * Money("12"))
                                .replace(" ", "")})
            if 'rentekostnader_total' in self.data.keys():
                tax_form.update({'rentekostnader_total': (
                        Money(self.data["rentekostnader_total"]) * Money("12"))
                                .replace(" ", "")})
            if 'andre_inntekter_total' in self.data.keys():
                tax_form.update({'andre_inntekter_total': (
                        Money(self.data["andre_inntekter_total"]) * Money("12"))
                                .replace(" ", "")})
            if 'leieinntekt_total' in self.data.keys():
                tax_form.update({'leieinntekt_total': (
                        Money(self.data["leieinntekt_total"]) * Money("12"))
                                .replace(" ", "")})
            tax_data = SkatteetatenTaxProcessing(tax_data=tax_form).skatteetaten_tax_info
            self.set_line_edits("", line_edits=self.tax_output, data=tax_data)