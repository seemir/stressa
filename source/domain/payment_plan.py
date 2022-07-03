# -*- coding: utf-8 -*-
"""
Module containing implementation of Mortgage Plan

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from datetime import datetime
import pandas as pd

from source.util import Assertor

from .fixed_rate import FixedRate
from .entity import Entity
from .money import Money


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
        return [""] + [str(date.date()) for date in
                       pd.date_range(start=self.start_date, periods=self.interval * self.period,
                                     freq=self.frequency)]

    def fixed_payment_list(self):
        """
        method for producing list of fixed payment

        """
        fixed_payment = FixedRate.periodical_payments(self.interest_rate, self.interval,
                                                      self.period, self.amount)
        return [0] + [int(fixed_payment) for _ in range(self.interval * self.period)]

    def fixed_mortgage_plan(self):
        """
        method for creating mortgage plan

        """
        index_list = []
        dates_list = []
        payment_list = []
        interest_list = []
        principal_list = []
        outstanding_list = []

        outstanding_amount = self.amount

        for i, payment in enumerate(self.fixed_payment_list()):
            index_list.append(i)
            if i == 0:
                dates_list.append("")
                payment_list.append("-" + Money(str(outstanding_amount)).value())
                interest_list.append("")
                principal_list.append("")
                outstanding_list.append(Money(str(outstanding_amount)).value())
            else:
                dates_list.append(self.period_list()[i])
                interest_amount = round(
                    outstanding_amount * (self.interest_rate / self.interval / 100))

                if i == len(self.fixed_payment_list()) - 1:
                    principal_amount = round(outstanding_amount)
                    payment = round(principal_amount + interest_amount)
                else:
                    principal_amount = round(payment - interest_amount)
                    payment = round(payment)

                outstanding_amount = round(outstanding_amount - principal_amount)

                payment_list.append(Money(str(payment)).value())
                interest_list.append(Money(str(interest_amount)).value())
                principal_list.append(Money(str(principal_amount)).value())
                outstanding_list.append(Money(str(outstanding_amount)).value())

        df = pd.DataFrame.from_dict(
            {'Termin': index_list, 'T.beløp': payment_list, 'Renter': interest_list,
             'Avdrag': principal_list, 'Restgjeld': outstanding_list})
        df.to_csv('fixed_mortgage_plan', sep=";", index=False)
