# -*- coding: utf-8 -*-

"""
Email value object module

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import re

from source.util import InvalidEmailError, LOGGER, Assertor

from .value import Value


class Email(Value):
    """
    Email value object implementation

    """

    @staticmethod
    def validate_email(email: str):
        """
        Method for validating a email according to regrex

        Parameters
        ----------
        email    : str
                  string to be validated

        """
        valid_email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+"
                                 r"\.[a-zA-Z0-9-.]+$)").search(email)
        if not valid_email:
            raise InvalidEmailError("'{}' is an invalid email".format(email))

    def __init__(self, email: str):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        email   : str
                  email

        """
        super().__init__()
        try:
            Assertor.assert_data_types([email], [str])
            self.validate_email(email)
            self._email = email
            LOGGER.success(
                "created '{}'".format(self.__class__.__name__))
        except Exception as email_error:
            LOGGER.exception(email_error)
            raise email_error

    @property
    def email(self):
        """
        email getter

        Returns
        -------
        out     : str
                  active email
        """
        return self._email

    @email.setter
    def email(self, email_):
        """
        email setter

        Parameters
        ----------
        email_  : str
                  new email to be set

        """
        Assertor.assert_data_types([email_], [str])
        self.validate_email(email_)
        self._email = email_

    def format_email(self):
        """
        method that returns formatted email, i.e. in lower case

        Returns
        -------
        out     : str
                  formatted email

        """
        email = self.email
        formatted = email.lower()
        LOGGER.info("format email '{}' to -> '{}'".format(email, formatted))
        return formatted