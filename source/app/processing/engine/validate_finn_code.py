# -*- coding: utf-8 -*-
"""
Validate Finn code validator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation
from ...connectors import Finn


class ValidateFinnCode(Operation):
    """
    Operation for validating a Finn code

    """

    @Tracking
    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        finn_code   : str
                      finn_code to be validated

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([finn_code], [str])
        super().__init__(name=self.name, desc="rules: {} \\n id: Validate Finn Code".format(
            Finn.rules()))
        self.finn_code = finn_code

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : str
                      validated Finn code str

        """
        Finn(self.finn_code).validate_finn_code()
        return self.finn_code
