# -*- coding: utf-8 -*-

__author__ = 'Samir Adrik'
__email__ = 'samir.adrik@gmail.com'

from source.app import MortgageAnalysisProcess

mortgage_data = {'arsinntekt': 699999, 'egenkapital': 800000, 'intervall': 'Måned',
                 'laneperiode': '25 år', 'lanetype': 'Sammenligning',
                 'nettolikviditet': 21000, 'startdato': '01.06.2023'}

analysis = MortgageAnalysisProcess(mortgage_data)

print(analysis.mortgage)
