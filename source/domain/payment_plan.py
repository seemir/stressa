# -*- coding: utf-8 -*-
"""
Module containing implementation of Mortgage Plan

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from datetime import datetime
import pandas as pd
import numpy as np

from source.util import Assertor

from .fixed_rate import FixedRate
from .entity import Entity
from .money import Money
from .share import Share


class PaymentPlan(Entity):
    """
    Implementation of Payment Plan entity

    """
    _interval_mapping = {"Årlig": 1, "Halvårlig": 2, "Kvartalsvis": 4, "Annenhver måned": 6,
                         "Månedlig": 12, "Semi-månedlig": 24, "Annenhver uke": 26, "Ukentlig": 52}

    _frequency_mapping = {"Årlig": pd.DateOffset(years=1),
                          "Halvårlig": pd.DateOffset(months=6),
                          "Kvartalsvis": pd.DateOffset(months=3),
                          "Annenhver måned": pd.DateOffset(months=2),
                          "Månedlig": pd.DateOffset(months=1),
                          "Semi-månedlig": "SMS",
                          "Annenhver uke": pd.DateOffset(weeks=2),
                          "Ukentlig": pd.DateOffset(weeks=1)}

    def __init__(self, interest_rate: str, interval: str, period: str, amount: str,
                 start_date: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        interest_rate       : str
                              interest_rate to be established
        interval            : str
                              payment interval
        period              : str
                              number of years for mortgage
        amount              : str
                              mortgage amount
        start_date          : str
                              start date

        """
        super().__init__()
        Assertor.assert_data_types([interest_rate, interval, period, amount, start_date],
                                   [str, str, str, str, str])
        self._interest_rate = float(interest_rate.replace(" %", ""))
        self._interval = self.interval_mapping[interval]
        self._interval_name = interval
        self._period = int(period.replace(" år", ""))
        self._amount = int(amount.replace(" kr", "").replace(" ", ""))
        self._start_date = datetime.strptime(start_date, "%d.%m.%Y").strftime('%Y-%m-%d')
        self._frequency = self.frequency_mapping[interval]

    @property
    def frequency(self):
        """
        frequency getter

        """
        return self._frequency

    @property
    def frequency_mapping(self):
        """
        frequency mapping getter

        """
        return self._frequency_mapping

    @property
    def interval_mapping(self):
        """
        interval mapping getter

        """
        return self._interval_mapping

    @property
    def interest_rate(self):
        """
        interest rate getter

        """
        return self._interest_rate

    @property
    def interval(self):
        """
        interval getter

        """
        return self._interval

    @property
    def interval_name(self):
        """
        interval getter

        """
        return self._interval_name

    @property
    def period(self):
        """
        period getter

        """
        return self._period

    @property
    def amount(self):
        """
        amount rate getter

        """
        return self._amount

    @property
    def start_date(self):
        """
        start_date getter

        """
        return self._start_date

    def period_list(self):
        """
        method for producing list of periods

        """
        return [""] + [datetime.strptime(str(date.date()), '%Y-%m-%d').strftime('%d.%m.%Y') for date
                       in pd.date_range(start=self.start_date, periods=self.interval * self.period,
                                        freq=self.frequency)]

    def fixed_mortgage_plan(self):
        """
        method for creating fixed mortgage plan

        """
        df = pd.DataFrame(columns=['Termin', 'Dato', 'T.beløp', 'T.beløp.total', 'Renter',
                                   'Renter.total', 'Avdrag', 'Avdrag.total', 'Restgjeld'],
                          dtype='float')

        df["Termin"] = list(range(len(self.period_list())))
        df["Dato"] = self.period_list()

        df["T.beløp"] = Money(str(int(
            round(FixedRate.periodical_payments(self.interest_rate, self.interval, self.period,
                                                self.amount))))).value()

        df.at[0, "T.beløp"] = "0 kr"

        df["T.beløp.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["T.beløp"])))]

        df["Avdrag"] = [Money(str(round((float(val.replace(" kr", "").replace(" ", "")) - (
                self.interest_rate / self.interval / 100) * self.amount) *
                                        ((1 + self.interest_rate / self.interval / 100) ** (
                                                i - 1))))).value() for i, val in
                        enumerate(df["T.beløp"])]

        df.at[0, "Avdrag"] = "0 kr"

        df["Avdrag.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["Avdrag"])))]

        df["Renter"] = [Money(str(value)).value() for value in
                        df["T.beløp"].str.replace(" kr", "").str.replace(" ", "").astype(int) - df[
                            "Avdrag"].str.replace(" kr", "").str.replace(" ", "").astype(int)]

        df["Renter.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["Renter"])))]

        df["Restgjeld"] = [Money(str(value)).value() for value in
                           -1 * (df["Avdrag.total"].str.replace(" kr", "")
                                 .str.replace(" ", "").astype(int) - self.amount)]

        df.at[self.period * self.interval, "Avdrag"] = df.at[
            self.period * self.interval - 1, "Restgjeld"]

        df["Avdrag.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["Avdrag"])))]

        df["Restgjeld"] = [Money(str(value)).value() for value in
                           -1 * (df["Avdrag.total"].str.replace(" kr", "")
                                 .str.replace(" ", "").astype(int) - self.amount)]

        df["T.beløp"] = [Money(str(value)).value() for value in
                         df["Renter"].str.replace(" kr", "").str.replace(" ", "").astype(int) + df[
                             "Avdrag"].str.replace(" kr", "").str.replace(" ", "").astype(int)]

        df["T.beløp.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["T.beløp"])))]

        start_date = df.at[1, "Dato"]
        end_date = df.at[self.period * self.interval, "Dato"]
        total_interest = df.at[self.period * self.interval, "Renter.total"]
        total_payment = df.at[self.period * self.interval, "T.beløp.total"]
        total_periods = str(df.at[self.period * self.interval, "Termin"])
        termin_year = str(self.interval) + f" ({self.interval_name})"
        years = str(self.period) + ' år'
        interest = str(self.interest_rate) + ' %'
        amount = df.at[self.period * self.interval, "Avdrag.total"]

        payment_share = Share(Money(total_payment), Money(total_payment)).value
        interest_share = Share(Money(total_interest), Money(total_payment)).value
        principal_share = Share(Money(amount), Money(total_payment)).value

        return {"nedbetalingsplan_annuitet": df.to_dict(), "start_dato_annuitet": start_date,
                "slutt_dato_annuitet": end_date, "total_rente_annuitet": total_interest,
                "total_belop_annuitet": total_payment, "total_termin_annuitet": total_periods,
                "aar_annuitet": years, "termin_aar_annuitet": termin_year, "laan_annuitet": amount,
                "rente_annuitet": interest,
                'nedbetalingsplan_annuitet_overview': self.aggregate_plan(df),
                'total_belop_andel_annuitet': payment_share,
                'total_rente_andel_annuitet': interest_share,
                'laan_andel_annuitet': principal_share}

    def serial_mortgage_plan(self):
        """
        method for creating serial mortgage plan

        """
        df = pd.DataFrame(columns=['Termin', 'Dato', 'T.beløp', 'T.beløp.total', 'Renter',
                                   'Renter.total', 'Avdrag', 'Avdrag.total', 'Restgjeld'],
                          dtype='float')

        df["Termin"] = list(range(len(self.period_list())))
        df["Dato"] = self.period_list()

        df["Avdrag"] = ["0 kr"] + ([Money(
            str(int(round(self.amount / (self.interval * self.period))))).value()] * (
                                           len(self.period_list()) - 1))

        df["Avdrag.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["Avdrag"])))]

        df["Restgjeld"] = [Money(str(value)).value() for value in
                           -1 * (df["Avdrag.total"].str.replace(" kr", "")
                                 .str.replace(" ", "").astype(int) - self.amount)]

        df.at[self.period * self.interval, "Avdrag"] = df.at[
            self.period * self.interval - 1, "Restgjeld"]

        df["Avdrag.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["Avdrag"])))]

        df["Restgjeld"] = [Money(str(value)).value() for value in
                           -1 * (df["Avdrag.total"].str.replace(" kr", "")
                                 .str.replace(" ", "").astype(int) - self.amount)]

        df["Renter"] = [Money(str(int(round(val)))).value() if i != 0 else "0 kr" for i, val in
                        enumerate(df["Restgjeld"].shift(1).fillna("0 kr").str.replace(" kr", "") \
                                  .str.replace(" ", "").astype(int) * (
                                          self.interest_rate / self.interval / 100))]
        df["Renter.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["Renter"])))]

        df["T.beløp"] = [Money(str(value)).value() for value in
                         df["Renter"].str.replace(" kr", "").str.replace(" ", "").astype(int) + df[
                             "Avdrag"].str.replace(" kr", "").str.replace(" ", "").astype(int)]
        df["T.beløp.total"] = [Money(str(value)).value() for value in np.cumsum(list(
            int(value.replace(" kr", "").replace(" ", "")) if i != 0 else 0 for i, value in
            enumerate(df["T.beløp"])))]

        start_date = df.at[1, "Dato"]
        end_date = df.at[self.period * self.interval, "Dato"]
        total_interest = df.at[self.period * self.interval, "Renter.total"]
        total_payment = df.at[self.period * self.interval, "T.beløp.total"]
        total_periods = str(df.at[self.period * self.interval, "Termin"])
        termin_year = str(self.interval) + f" ({self.interval_name})"
        years = str(self.period) + ' år'
        interest = str(self.interest_rate) + ' %'
        amount = df.at[self.period * self.interval, "Avdrag.total"]

        payment_share = Share(Money(total_payment), Money(total_payment)).value
        interest_share = Share(Money(total_interest), Money(total_payment)).value
        principal_share = Share(Money(amount), Money(total_payment)).value

        return {"nedbetalingsplan_serie": df.to_dict(), "start_dato_serie": start_date,
                "slutt_dato_serie": end_date, "total_rente_serie": total_interest,
                "total_belop_serie": total_payment, "total_termin_serie": total_periods,
                "aar_serie": years, "termin_aar_serie": termin_year, "laan_serie": amount,
                "rente_serie": interest,
                'nedbetalingsplan_serie_overview': self.aggregate_plan(df),
                'total_belop_andel_serie': payment_share,
                'total_rente_andel_serie': interest_share,
                'laan_andel_serie': principal_share}

    @staticmethod
    def aggregate_plan(df: pd.DataFrame):
        """
        method for aggregating values in a pandas dataframe

        """
        agg_df = pd.DataFrame()

        agg_df['Termin'] = df.loc[1:, ]['Termin']
        agg_df['Dato'] = df.loc[1:, ]['Dato']

        agg_df['T.beløp'] = df.loc[1:, ]['T.beløp'].str.replace(" kr", "") \
            .str.replace(" ", "").astype(int)
        agg_df['T.beløp.total'] = df.loc[1:, ]['T.beløp.total'].str.replace(" kr", "") \
            .str.replace(" ", "").astype(int)
        agg_df['Renter'] = df.loc[1:, ]['Renter'].str.replace(" kr", "") \
            .str.replace(" ", "").astype(int)
        agg_df['Renter.total'] = df.loc[1:, ]['Renter.total'].str.replace(" kr", "") \
            .str.replace(" ", "").astype(int)
        agg_df['Avdrag'] = df.loc[1:, ]['Avdrag'].str.replace(" kr", "") \
            .str.replace(" ", "").astype(int)
        agg_df['Avdrag.total'] = df.loc[1:, ]['Avdrag.total'].str.replace(" kr", "") \
            .str.replace(" ", "").astype(int)
        agg_df = agg_df.loc[1:, ].reset_index(drop=True)

        final_df = pd.DataFrame()
        final_df['T.beløp'] = agg_df.groupby(pd.to_datetime(agg_df['Dato'])
                                             .dt.year)['T.beløp'].agg(['max'])
        final_df['T.beløp.total'] = agg_df.groupby(pd.to_datetime(agg_df['Dato'])
                                                   .dt.year)['T.beløp'].agg(['sum'])
        final_df['T.beløp.total'] = final_df['T.beløp.total'].cumsum()

        final_df['Renter'] = agg_df.groupby(pd.to_datetime(agg_df['Dato'])
                                            .dt.year)['Renter'].agg(['max'])
        final_df['Renter.total'] = agg_df.groupby(pd.to_datetime(agg_df['Dato'])
                                                  .dt.year)['Renter'].agg(['sum'])
        final_df['Renter.total'] = final_df['Renter.total'].cumsum()

        final_df['Avdrag'] = agg_df.groupby(pd.to_datetime(agg_df['Dato'])
                                            .dt.year)['Avdrag'].agg(['max'])
        final_df['Avdrag.total'] = agg_df.groupby(pd.to_datetime(agg_df['Dato'])
                                                  .dt.year)['Avdrag'].agg(['sum'])
        final_df['Avdrag.total'] = final_df['Avdrag.total'].cumsum()

        final_df['År'] = range(0, len(final_df))

        aar = final_df.pop('År')
        final_df.insert(0, 'År', aar)

        final_df['T.beløp'] = [Money(value).value() for value in final_df['T.beløp'].astype(str)]
        final_df['T.beløp.total'] = [Money(value).value() for value in
                                     final_df['T.beløp.total'].astype(str)]
        final_df['Renter'] = [Money(value).value() for value in final_df['Renter'].astype(str)]
        final_df['Renter.total'] = [Money(value).value() for value in
                                    final_df['Renter.total'].astype(str)]
        final_df['Avdrag'] = [Money(value).value() for value in final_df['Avdrag'].astype(str)]
        final_df['Avdrag.total'] = [Money(value).value() for value in
                                    final_df['Avdrag.total'].astype(str)]

        final_df = final_df.reset_index(drop=True)

        return final_df.to_dict()
