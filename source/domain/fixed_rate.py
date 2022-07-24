# -*- coding: utf-8 -*-
"""
Fixed rate mortgage Entity

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from typing import Union
import numpy as np

from source.util import Assertor

from .mortgage import Mortgage


class FixedRate(Mortgage):
    """
    Implementation of the Fixed Rate mortgage

    """
    _interval_mapping = {"Årlig": 1, "Halvårlig": 2, "Kvartalsvis": 4, "Annenhver måned": 6,
                         "Månedlig": 12, "Semi-månedlig": 24, "Annenhver uke": 26, "Ukentlig": 52}

    @staticmethod
    def periodical_payments(interest_rate: (float, str), interval: (int, str),
                            period: (int, str), amount: Union[int, float, str]):
        """
        method for calculating the periodical payment in a fixed rate mortgage

        Parameters
        ----------
        interest_rate   : float, str
                          yearly interest rate
        interval        : int, str
                          interval for which to pay
        period          : int, str
                          number of years for the mortgage
        amount          : int, float, str
                          mortgage amount

        Returns
        -------
        out             : float
                          periodical amount to pay

        """
        Assertor.assert_data_types([interest_rate, interval, period, amount],
                                   [(float, str), (int, str), (int, str), (int, float, str)])

        if isinstance(interest_rate, str):
            interest_rate = float(interest_rate.replace(" %", "").replace(" ", ""))
        if isinstance(interval, str):
            interval = {"Årlig": 1, "Halvårlig": 2, "Kvartalsvis": 4, "Annenhver måned": 6,
                        "Månedlig": 12, "Semi-månedlig": 24, "Annenhver uke": 26,
                        "Ukentlig": 52}[interval]
        if isinstance(period, str):
            period = int(period.replace(" år", "").replace(" ", ""))
        if isinstance(amount, str):
            amount = float(amount.replace(" kr", "").replace(" ", ""))

        interest_foot = interest_rate / 100 / interval
        return int(round((interest_foot / (1 - (1 + interest_foot) ** -(interval * period)))
                         * amount))

    def __init__(self, data: dict):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        data        : dict
                      mortgage information

        """
        super().__init__(data=data)
        self._interval = self._interval_mapping[self.mortgage_data['intervall']]
        self._period = int(self.mortgage_data['laneperiode'].replace(" år", ""))
        self._start_date = self.mortgage_data['startdato']
        self._equity = float(self.mortgage_data['egenkapital'].replace(" kr", "").replace(" ", ""))
        self._net_liquidity = float(
            self.mortgage_data['netto_likviditet'].replace(" kr", "").replace(" ", ""))
        self._amount = float(
            self.mortgage_data['personinntekt_total_aar'].replace(" kr", "").replace(" ", "")) * 5 \
            if 'belaning' not in data.keys() else data['belaning']

    @property
    def interval_mapping(self):
        """
        interval mapping getter

        """
        return self._interval_mapping

    @property
    def period(self):
        """
        period getter

        """
        return self._period

    @property
    def interval(self):
        """
        interval getter

        """
        return self._interval

    @property
    def start_date(self):
        """
        start date getter

        """
        return self._start_date

    @property
    def equity(self):
        """
        equity getter

        """
        return self._equity

    @property
    def net_liquidity(self):
        """
        net liquidity getter

        """
        return self._net_liquidity

    @property
    def amount(self):
        """
        amount getter

        """
        return self._amount

    def calculate_stress_rate(self):
        """
        method for calculating the max stress rate

        """
        stress_rates = {round(self.periodical_payments(i, self.interval, self.period,
                                                       self.amount)): round(i, 3) for i in
                        np.arange(0.001, 30.000, 0.001)}

        net_liquidity = self.net_liquidity if self.interval == 12 else \
            (self.net_liquidity * 12) / self.interval

        diff_rates = {abs(net_liquidity - liquidity): rates for liquidity, rates in
                      stress_rates.items() if net_liquidity - liquidity > 0}
        stress_rate = list(diff_rates.values())[-1]
        return str(stress_rate) + ' %'
