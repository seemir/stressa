# -*- coding: utf-8 -*-
"""
Module with logic for the SubModel class

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from abc import abstractmethod

from source.util import Assertor, Tracking

from .operation import Operation


class SubModel(Operation):
    """
    Implementation of SubModel class which is both a process and an operation

    """

    @Tracking
    def __init__(self, name: str, desc: str):
        """
        Constructor / Instantiating class

        Parameters
        ----------
        name        : str
                      name of operation or process
        desc        : str
                      description of operation process

        """
        self.name = name
        Assertor.assert_data_types([name, desc], [str, str])
        self.desc = desc
        Operation.__init__(self, name=self.name, desc=self.desc,
                           label="\\<SubModel ({})\\> \n Process: {} \\n id: {}".format(
                               self.__class__.__name__, self.name, self.desc))

    @abstractmethod
    def run(self):
        pass
