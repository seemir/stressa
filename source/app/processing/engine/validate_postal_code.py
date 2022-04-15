# -*- coding: utf-8 -*-
"""
Validate Finn code operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from ...connectors import Posten

from .operation import Operation


class ValidatePostalCode(Operation):
    """
    Operation for validating a Norwegian Postal Code

    """

    @Tracking
    def __init__(self, postal_code: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        postal_code    : str
                         postal_code to be validated

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([postal_code], [str])
        super().__init__(name=self.name,
                         desc="rules: {} \\n id: Validate Postal Code".format(Posten.rules()))
        self.zip_code = postal_code

    @Tracking
    def run(self):
        """
        method for running the operation

        Returns
        -------
        out         : str
                      validated Postal Code str

        """
        Posten(self.zip_code).validate_postal_code()
        return self.zip_code
