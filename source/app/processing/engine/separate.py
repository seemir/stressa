# -*- coding: utf-8 -*-
"""
Module with Separate operation

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util import Assertor, Tracking

from .operation import Operation


class Separate(Operation):
    """
    The separate operation splits a list of dictionaries into a dict of dicts

    """

    @Tracking
    def __init__(self, data: list, desc: str):
        """
        Constructor / Instantiate the class.

        Parameters
        ----------
        data        : list
                      data to separate
        desc        : str
                      description of operation

        """
        self.name = self.__class__.__name__
        Assertor.assert_data_types([data, desc], [list, str])
        super().__init__(name=self.name, desc="id: {}".format(desc))
        self.data = data

    @Tracking
    def run(self):
        """
        method for running operation

        Returns
        -------
        out         : dict
                      dictionary with data

        """
        output = {}
        for dictionary in self.data:
            if "id" in dictionary.keys():
                identifier = dictionary["id"].lower()
                if identifier == "1001":
                    output.update({"rating_roads": dictionary})
                elif identifier == "1002":
                    output.update({"rating_gardens": dictionary})
                elif identifier == "1003":
                    output.update({"rating_safety": dictionary})
                elif identifier == "1004":
                    output.update({"rating_environment": dictionary})
                elif identifier == "1005":
                    output.update({"rating_noise": dictionary})
                elif identifier == "1006":
                    output.update({"rating_kids_area": dictionary})
                elif identifier == "1007":
                    output.update({"rating_schools": dictionary})
                elif identifier == "1008":
                    output.update({"rating_kindergardens": dictionary})
                elif identifier == "1009":
                    output.update({"rating_hiking": dictionary})
                elif identifier == "1010":
                    output.update({"rating_public_transport": dictionary})
                elif identifier == "2016":
                    output.update({"rating_activity": dictionary})
                elif identifier == "2019":
                    output.update({"rating_serving": dictionary})
                else:
                    output.update({identifier: dictionary})
            else:
                output.update(dictionary)
        return output
