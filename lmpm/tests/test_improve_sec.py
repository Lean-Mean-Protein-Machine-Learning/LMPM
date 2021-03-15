#!/usr/bin/env python
# coding: utf-8
"""
Write tests for the improve_sec.py functions.
"""


import lmpm.improve_sec as improve_sec


def test_get_residue_positions():
    positions = ["1,3-5,8", "1,4", "Space-aliens are coming!", '']

    for places in positions:

        try:
            improve_sec.get_residue_positions(places)

        except Exception as exep:
            assert isinstance(exep, ValueError), 'The position is a list of integers or ranges defined as: "integer-integer", but an error occured'


def test_optimize_sequence():
    sequence = 'ALIENSRCMING'
    organism = ['human', 'yeast', 'ecoli', 'space aliens']
    target_loc = ['secreted', 'membrane', 'cytoplasm', 'Zeta Reticuli']
    positions = ["1,3-5,8", "1,4", "Space-aliens are coming!", '']

    for places in positions:
        try:
            res_posit = improve_sec.get_residue_positions(places)
            improve_sec.optimize_sequence(sequence, organism[1], target_loc[1], False, res_posit)

        except Exception as exep:
            assert isinstance(exep, ValueError), "The correct input protein length was entered, but an error occured in optimize_sequence()."


def test_plot_optimization():
    sequence = 'ALIENSRCMING'
    organism = ['human', 'yeast', 'ecoli', 'space aliens']
    target_loc = ['secreted', 'membrane', 'cytoplasm', 'Zeta Reticuli']
    positions = ["1,3-5,8", "1,4", "Space-aliens are coming!", '']

    for places in positions:
        try:
            res_posit = improve_sec.get_residue_positions(places)
            mutated_scores, initial_score =  improve_sec.optimize_sequence(sequence, organism[1], target_loc[1], False, res_posit)
            improve_sec.plot_optimization(mutated_scores, initial_score, dpi=100)

        except Exception as exep:
            assert isinstance(exep, ValueError), " The correct size inputs were entered, but an error occured in plot_optimization() "






