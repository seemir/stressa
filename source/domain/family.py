# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.util.assertor import Assertor
from source.domain.entity import Entity
from source.domain.female import Female
from source.domain.male import Male


class Family(Entity):

    @staticmethod
    def assert_guardianship(family):
        """
        Assert that guardianship is present in family object, raises ValueError if not present.

        Parameters
        ----------
        family      : list
                      list of Person (Male or Female) instances

        """
        if not len(family) > 2:
            for family_member in family:
                if family_member.alder < '18':
                    raise ValueError("family not possible without guardianship, i.e. family must "
                                     "have atleast one person older than 18.")

    @staticmethod
    def assert_family(family):
        """
        Assert that family argument is a list of person object. Raises TypeError if family is not a
        list of person (Male, Female) objects or ValueError if family has no guardianship.

        Parameters
        ----------
        family      : list
                      list of person objects

        """
        if not isinstance(family, list):
            raise TypeError(
                "expected type '{}', got '{}' instead".format(list.__name__,
                                                              type(family).__name__))
        if not family:
            raise ValueError("family_members cannot be empty, got '[]'")

        for family_member in family:
            Assertor.assert_date_type({family_member: (Male, Female)})
        Family.assert_guardianship(family)

    def __init__(self, family_members=None, income=0, cars=0):
        """
        Constructor / Instantiate the class

        Parameters
        ----------
        family_members  : list
                          list of Person (Male or Female) instances
        income          : int, float, str
                          gross yearly income
        cars            : int, str
                          number of cars in the family

        """
        super().__init__()
        self.assert_family(family_members)
        Assertor.assert_date_type({income: (int, float, str), cars: (int, str)})
        for arg in [income, cars]:
            Assertor.assert_non_negative(arg)

        self._family_members = family_members
        self._inntekt = str(income)
        self._antall_biler = str(cars)

    @property
    def family_members(self):
        """
        family_members getter

        Returns
        -------
        out         : list
                      all active family_members

        """
        return self._family_members

    @family_members.setter
    def family_members(self, members):
        """
        family_members setter

        Parameters
        ----------
        members     : list of person (Male or Female) objects
                      a list of family_members to append to family

        """
        self.assert_family(members)
        self._family_members = members

    def add_family_members(self, family_members):
        """
        Append a list Male or Female family_member to family_members

        Parameters
        ----------
        family_members : list of Female or Male instances
                         family member to be appended

        """
        if isinstance(family_members, list):
            all(Assertor.assert_date_type({f: (Male, Female)}) for f in family_members)
            self._family_members.extend(family_members)
        else:
            Assertor.assert_date_type({family_members: (Male, Female)})
            self._family_members.extend([family_members])

    @property
    def inntekt(self):
        """
        income getter

        Returns
        -------
        out         : int, float
                      current gross yearly income

        """
        return self._inntekt

    @inntekt.setter
    def inntekt(self, income):
        """
        income setter

        Parameters
        ----------
        income      : int, float, str
                      new gross yearly income

        """
        Assertor.assert_date_type({income: (int, float, str)})
        Assertor.assert_non_negative(income)
        self._inntekt = str(income)

    @property
    def antall_biler(self):
        """
        cars setter

        Returns
        -------
        out     : str
                  number of cars in the family

        """
        return self._antall_biler

    @antall_biler.setter
    def antall_biler(self, cars):
        """
        cars setter

        Parameters
        ----------
        cars    : int, str
                  new number of cars to set in family

        """
        Assertor.assert_date_type({cars: (int, str)})
        Assertor.assert_non_negative(cars)
        self._antall_biler = str(cars)

    def get_properties(self):
        """
        return all active properties and values in a dictionary

        Returns
        -------
        Out     : dict
                  dictionary of all active properties

        """
        properties = dict(list(self.__dict__.items())[-2:])
        for i, family_member in enumerate(self.family_members):
            properties.update(
                {fam_member + str(i): prop_value for fam_member, prop_value in
                 family_member.__dict__.items()})
        return {name[1:]: value for name, value in properties.items()}
