# -*- coding: utf-8 -*-

"""
Module for Operation for reading settings

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import os
import json

from source.util import Assertor, Tracking

from .operation import Operation


class ReadSettings(Operation):
    """
    Implementation of Operation

    """
    dept_mapping = {'4.0 x': 4.0, '4.5 x': 4.5, '5.0 x': 5.0, '5.5 x': 5.5, '6.0 x': 6}

    @Tracking
    def __init__(self, setting: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        setting    : str
                     name of setting to get

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([setting], [str])
        Assertor.assert_arguments([setting],
                                  [{"settings": ("egenkapital_krav", "gjeldsgrad", "stresstest")}])
        super().__init__(name=self.name,
                         desc="setting : {}".format(setting))
        self.setting = setting

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out     : float, int


        """
        up = os.path.dirname
        settings_dir = up(__file__) + '\\tmp'

        if os.path.exists(settings_dir):
            with open(settings_dir + '\\settings.json', 'r') as fp:
                try:
                    settings = json.load(fp)
                    equity = settings['egenkapital_krav']
                    dept = settings['gjeldsgrad']
                    stress = settings['stresstest']
                except Exception:
                    pass

        if self.setting == 'egenkapital_krav':
            setting = equity.replace(" %", ".0 %")
        elif self.setting == 'gjeldsgrad':
            setting = self.dept_mapping[dept]
        else:
            setting = stress.replace(" %", "")

        return {"factor": setting}
