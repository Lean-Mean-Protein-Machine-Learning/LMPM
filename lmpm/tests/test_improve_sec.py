#!/usr/bin/env python
# coding: utf-8
"""
Write tests for the improve_sec.py functions.
"""


import lmpm.improve_sec as improve_sec
import matplotlib.pyplot as plt


def test_get_residue_positions():
    positions = ["1,3-5,8", "1,4", "Space-aliens are coming!", '']

    for places in positions:

        try:
            improve_sec.get_residue_positions(places)
        except Exception as exep:
            assert isinstance(exep, ValueError), 'Passing an incorrect list of residues did not raise a ValueError'


def test_optimize_sequence():
    sequence = 'ALIENSRCMING'
    organism = ['human', 'yeast', 'ecoli', 'space aliens']
    target_loc = ['secreted', 'membrane', 'cytoplasm', 'Zeta Reticuli']
    positions = ["1,3-5","120,150","Space-aliens are coming!","1-12"]

    for places in positions:
        try:
            improve_sec.optimize_sequence(sequence, organism[1], target_loc[1], False, places)

        except Exception as exep:
            assert isinstance(exep, ValueError), "Passing an incorrect list of residues did not raise a ValueError."

    # test the function without position argument too
    try:
        mutated_scores, initial_score = improve_sec.optimize_sequence(sequence, organism[1], target_loc[1], False)
    except Exception as exep:
        assert isinstance(exep, ValueError), "Trying to mutate all positions did not raise a ValueError."


def test_plot_optimization():
    sequence = 'ALIENSRCMING'
    organism = 'human'
    target_loc = 'membrane'
    position = '1,3'
    
    # get some correct input data
    mutated_scores, initial_score =  improve_sec.optimize_sequence(sequence, organism, target_loc, False, position)

    # generate an incorrect format for input data
    mut_scores_options = [mutated_scores, {'incorrect_format':0.9,'incorrect_loc':0.1}]
    
    # try passing correct and incorrect values for mutated_scores
    for mut_sc in mut_scores_options:
        try:
            improve_sec.plot_optimization(mut_sc, initial_score, dpi=100)
        except Exception as exep:
            assert isinstance(exep, TypeError), "Passing incorrect format for mutated_scores did not raise TypeError"

    # try passing incorrect type for initial_score
    try:
        improve_sec.plot_optimization(mutated_scores, initial_score=['alienscore'], plot_inplace = False, dpi=100)
    except Exception as exep:
        assert isinstance(exep, TypeError), "Passing incorrect format for initial_score did not raise TypeError"
    
    # try passing incorrect type for dpi
    try:
        improve_sec.plot_optimization(mutated_scores, initial_score, True, dpi='aliensrcoming')
    except Exception as exep:
        assert isinstance(exep, TypeError), "Passing incorrect format for dpi did not raise TypeError"

    # try getting the figure as return
    figure_res = improve_sec.plot_optimization(mutated_scores, initial_score, False, dpi=100)
    assert type(figure_res) == plt.Figure, 'Trying to get the figure in return did not generate a matplotlib.Figure'

def test_top_mutations():
    sequence = 'ALIENSRCMING'
    organism = 'human'
    target_loc = 'membrane'
    position = '1,3'

    mutated_scores, initial_score =  improve_sec.optimize_sequence(sequence, organism, target_loc, False, position)
    try:
        improve_sec.top_mutations(mutated_scores, initial_score, 'aliens')
    except Exception as exep:
        assert isinstance(exep, TypeError), "Passing a non-integer as top_results did not return a type error"

    result = improve_sec.top_mutations(mutated_scores, initial_score, 10)
    assert type(result) == pd.DataFrame, "The result of top_mutations is not a DataFrame"