"""
This file contains functions to improve secretion scores.

It takes in a sequence (dna, amino acid in 1 or 3 letter code), the target secretion location (cyto/transm/secret)
and (optionally) an organism that the user provides.
Mutates the sequence at all positions for all amino acids (if it is shorter than X amino acids, if not it would take too long).
Returns a plot similar to an SSM (it is nothing more than a heatmap with position at horizontal axis and amino acid at vertical axis)
with colors indicating better probability for the target secretion location or worse probability.

To get a better understanding on python imports, read: https://realpython.com/absolute-vs-relative-python-imports/
"""

import sys
import matplotlib as plt
import numpy as np
import pandas as pd

from predict import secretion_score



def secretion_optimization(sequence, organism, position, include_dg=False):
    """
    Introduces amino acid point mutation at given position to improve
    probability of given sequence to be part of the secreted class

    Args:
        sequence (str): amino acid sequence in single-letter format
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)
        position (int): given position where point mutations can occur
                        (where first residue is position 0)
        include_dg (Boolean): specify inclusion of additional features
                                (default=False)

    Returns:
        sequence (str): mutated amino acid sequence
        point_mutation_dict (dict): dictionary of point mutation amino acid
                                    and secretion score
    """
    # First, find the initial class and initial secretion score
    initial_class, initial_score = secretion_score(sequence, organism, include_dg)
    print('The initial sequence is:', sequence)
    print('The initial localization clas is:', initial_class)
    print('The initial probability of being in the secreted class is:', 
        initial_score)

    # Define list of amino acids
    amino_acids = ['G', 'A', 'L', 'M', 'F', 
                    'W', 'K', 'Q', 'E', 'S', 
                    'P', 'V', 'I', 'C', 'Y', 
                    'H', 'R', 'N', 'D', 'T']

    # Set up point mutations
    mutated_scores_list = []
    for residue in amino_acids:
        sequence_list = list(sequence)
        sequence_list[position] = residue
        mutated_sequence = "".join(sequence_list)
        mutated_class, mutated_score = secretion_score(
            sequence, organism, include_dg)
        mutated_scores_list.append(mutated_score)
        # Replace initial sequence if mutated secretion score is better
        if mutated_score > initial_score:
            sequence = mutated_sequence
            initial_score = mutated_score
            initial_class = mutated_class

    print('The mutated sequence is:', sequence)
    print('The mutated class is:', initial_class)
    print('The mutated probability of being in the secreted class is:',
        mutated_score)

    # Plot point mutations and scores
    plt.plot(amino_acids, mutated_scores_list)
    plt.xlabel('Amino Acid Point Mutation at Position %d' % position)
    plt.ylabel('Probability of Secretion Class')

    # Create dictionary of point mutations and scores
    point_mutation_dict = {amino_acids[i]: mutated_scores_list[i]
        for i in range(len(amino_acids))}

    return sequence, point_mutation_dict


def secretion_optimization_all_positions(sequence, organism):
    """
    create ssm like representation
    """


def optimize_secretion(sequence, organism, position):
    """
    Wrapper function.

    It would be great if we added a parameter position that can take in a list of positions
    so the user is free to mutate only one position or a few positions of the sequence. 
    If nothing is passed, we mutate all sequence.

    """

