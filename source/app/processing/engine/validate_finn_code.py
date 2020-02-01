# -*- coding: utf-8 -*-
"""
Validate Finn code validator

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor

from .operation import Operation
from ...scrapers import Finn


class ValidateFinnCode(Operation):
    """
    Operation for validating a Finn code

    """

    def __init__(self, finn_code: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        finn_code   : str
                      finn_code to be validated

        """
        Assertor.assert_data_types([finn_code], [str])
        self.name = self.__class__.__name__
        super().__init__(name=self.name, desc="rules: {} \\n id: Validate Finn Code".format(
            Finn.rules()))
        self.finn_code = finn_code

    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : str
                      validated Finn code str

        """
        Finn.validate_finn_code(self.finn_code)
        return self.finn_code
