"""
This file contains functions to improve secretion scores.

It takes in a sequence (dna, amino acid in 1 or 3 letter code), the target secretion location (cyto/transm/secret)
and (optionally) an organism that the user provides.
Mutates the sequence at all positions for all amino acids (if it is shorter than X amino acids, if not it would take too long).
Returns a plot similar to an SSM (it is nothing more than a heatmap with position at horizontal axis and amino acid at vertical axis)
with colors indicating better probability for the target secretion location or worse probability.

To get a better understanding on python imports, read: https://realpython.com/absolute-vs-relative-python-imports/
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .predict import localization_score

amino_acids = ['G', 'A', 'L', 'M', 'F',
               'W', 'K', 'Q', 'E', 'S',
               'P', 'V', 'I', 'C', 'Y',
               'H', 'R', 'N', 'D', 'T']

def get_residue_positions(positions):
    """Converts a list of integers or range of residues to individual residue numbers.
    
    Args:
        positions: list of protein residues as integers or ranges.
            Example: [1,3-5,8]
            
    Returns:
        res_posit: list of individual residues.
            Example: [1,3,4,5,8]
    """
    
    # initialize list
    res_posit = np.array([])
    
    for item in positions:
        # split if contains a "-"
        item = np.array(item.split('-'), dtype='int')
        # if it contains a "-" the length will be 2
        if len(item) == 2:
            # create a range of integers from lower to higher value
            res_posit = np.append(res_posit, list(range(item[0], item[1]+1)))
        elif len(item) == 1:
            res_posit = np.append(res_posit, item)
        else:
            raise ValueError('The position should be a list of integers or ranges defined as: "integer-integer"')
    
    res_posit = np.array(np.unique(np.sort(res_posit)), dtype='int')
    
    return res_posit

# wrapper function
def optimize_sequence(sequence, organism, target_class, include_dg=False, positions=None):
    """
    Introduces amino acid point mutation at given position to improve
    probability of given sequence to be part of the secreted class

    Args:
        sequence (str): amino acid sequence in single-letter format
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)
        target_class (str): class of interest to optimize the sequence
                        (cytoplasm, membrane, secreted)
        include_dg (Boolean): specify inclusion of additional features
                                (default=False)
        positions (list): given position where point mutations can occur
                         (where first residue is position 1), example:
                         ['5','7-9',12]

    Returns:
        mutated_scores (pd.DataFrame): localization scores for each mutation
                        at each position
    """
    # First, find the initial class and initial secretion score for that class
    initial_class, initial_score = secretion_score(sequence, organism, target_class, include_dg)
    # Also find the probability of being from the target_class
#     print('The initial sequence is:', sequence)
#     print('The initial localization clas is:', initial_class)
#     print('The initial probability of being in the secreted class is:', 
#         initial_score)
    
    
    # if no position was specified mutate all
    if positions == None:
        res_poses = np.array(list(range(0,len(sequence))))
    else:
        # create test to check if position is a list
        res_poses = get_residue_positions(positions)
        # inform user that positions are 1 based so that they can usually work on that from a pdb file
        # convert positions to 0 based positions
        res_poses = res_poses - 1
        
        # check if largest position is within the protein length
        if np.max(res_poses)+1 > len(sequence):
            raise ValueError('You passed residue position '+str(np.max(res_poses)+1)+', which is larger than the protein length of '+str(len(sequence))+' residues.')
        else:
            pass

    mutated_scores = pd.DataFrame()
    
    for resid in res_poses:
#         print("running position", resid, "of", str(np.max(res_poses)))
        
        mut_score_pos = []
        
        for mutation in amino_acids:
            mutated_seq = sequence[:resid] + str(mutation) + sequence[resid+1:]
#             pred_score = 3
            pred_class, pred_score = secretion_score(mutated_seq, organism, target_class, include_dg)
            mut_score_pos.append(pred_score)
        
        mut_score_pos = pd.Series(mut_score_pos, index = amino_acids)
        
        original_name = str(sequence[resid]) + '_' + str(resid)
        
        mutated_scores[original_name] = mut_score_pos

    # an alternative would be returning the relative increment
    sns.heatmap(mutated_scores-initial_score, annot=False)
    plt.show()
    
    return mutated_scores