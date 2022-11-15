# -*- coding: utf-8 -*-

"""
Test module for Ssb payload logic

"""

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

import pytest as pt

from source.app import SsbPayload


class TestSsbPayload:
    """
    Test cases for the SsbPayload object

    """

    @staticmethod
    @pt.mark.parametrize("utlanstype", ["54", "66"])
    @pt.mark.parametrize("sektor", ["01", "25"])
    @pt.mark.parametrize("rentebinding", ["19", "22"])
    @pt.mark.parametrize("tid", ["202008"])
    def test_value_error_for_invalid_args(utlanstype, sektor, rentebinding, tid):
        """
        Testing that ValueError get thrown for invalid arguments

        """
        payload = SsbPayload()

        with pt.raises(ValueError):
            payload.utlanstype = [utlanstype]
        with pt.raises(ValueError):
            SsbPayload(utlanstype=[utlanstype])

        with pt.raises(ValueError):
            payload.sektor = [sektor]
        with pt.raises(ValueError):
            SsbPayload(sektor=[sektor])

        with pt.raises(ValueError):
            payload.rentebinding = [rentebinding]
        with pt.raises(ValueError):
            SsbPayload(rentebinding=[rentebinding])

        with pt.raises(ValueError):
            payload.tid = [tid]
        with pt.raises(ValueError):
            SsbPayload(tid=[tid])

    @staticmethod
    @pt.mark.parametrize("utlanstype", ["04", "70"])
    @pt.mark.parametrize("sektor", ["04b", "04a"])
    @pt.mark.parametrize("rentebinding", ["08", "12"])
    @pt.mark.parametrize("tid", ["2019M08"])
    def test_payload_prop_gets_set(utlanstype, sektor, rentebinding, tid):
        """
        Testing that arguments gets set in SsbPayload object via constructor

        """
        payload = SsbPayload([utlanstype], [sektor], [rentebinding], [tid])
        assert payload.utlanstype == [utlanstype]
        assert payload.sektor == [sektor]
        assert payload.rentebinding == [rentebinding]
        assert payload.tid == [tid]

    @staticmethod
    @pt.mark.parametrize("utlanstype", ["04", "70"])
    @pt.mark.parametrize("sektor", ["04b", "04a"])
    @pt.mark.parametrize("rentebinding", ["08", "12"])
    @pt.mark.parametrize("tid", ["2019M08"])
    def test_payload_prop_gets_setter(utlanstype, sektor, rentebinding, tid):
        """
        Testing that arguments gets set in SsbPayload object via setter

        """
        payload = SsbPayload()
        payload.utlanstype = [utlanstype]
        assert payload.utlanstype == [utlanstype]
        payload.sektor = [sektor]
        assert payload.sektor == [sektor]
        payload.rentebinding = [rentebinding]
        assert payload.rentebinding == [rentebinding]
        payload.tid = [tid]
        assert payload.tid == [tid]
