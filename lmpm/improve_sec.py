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
import matplotlib.colors as colors
import seaborn as sns

from .predict import predict_loc_simple

amino_acids = ['G', 'A', 'L', 'M', 'F',
               'W', 'K', 'Q', 'E', 'S',
               'P', 'V', 'I', 'C', 'Y',
               'H', 'R', 'N', 'D', 'T']

def get_residue_positions(positions):
    """Converts a list of integers or ranges of residues to individual residue numbers.
    
    Args:
        positions: string with a list of protein residues as integers or ranges.
            Example: "1,3-5,8"
            
    Returns:
        res_posit: list of individual residues.
            Example: [1,3,4,5,8]
    """
    
    # initialize list
    res_posit = np.array([])

    # preprocess string to get list
    positions = positions.split(',')

    for item in positions:
        # split if contains a "-"
        try:
            item = np.array(str(item).split('-'), dtype='int')
        except Exception as exep:
            raise ValueError('The position should be a list of integers or ranges defined as: "integer-integer"')

        # if it contains a "-" the length will be 2
        if len(item) == 2:
            # create a range of integers from lower to higher value
            res_posit = np.append(res_posit, list(range(item[0], item[1]+1)))
        elif len(item) == 1:
            res_posit = np.append(res_posit, item)
        
    res_posit = np.array(np.unique(np.sort(res_posit)), dtype='int')
    
    return res_posit

# wrapper function
def optimize_sequence(sequence, organism, target_class, include_dg=False, positions=None):
    """
    
    """
    # First, find the initial class and initial secretion score for that class
    initial_score = predict_loc_simple(sequence, organism, target_class, include_dg)
    # Also find the probability of being from the target_class
#     print('The initial sequence is:', sequence)
#     print('The initial localization clas is:', initial_class)
#     print('The initial probability of being in the secreted class is:', 
#         initial_score)
    
    # set a maximum of positions with time and plot maximum considerations
    
    
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

    # if specified more than 10 positions, return an error as it would take too much time.
    if len(res_poses) > 10:
        raise ValueError('The maximum number of residues to mutate is currently set at 10. Going over this maximum would take too much time with the current implementation, sorry.')

    mutated_scores = pd.DataFrame()
    
    for resid in res_poses:
#         print("running position", resid, "of", str(np.max(res_poses)))
        
        mut_score_pos = []
        
        for mutation in amino_acids:
            mutated_seq = sequence[:resid] + str(mutation) + sequence[resid+1:]
            pred_score = predict_loc_simple(mutated_seq, organism, target_class, include_dg)
            mut_score_pos.append(pred_score)
        
        mut_score_pos = pd.Series(mut_score_pos, index = amino_acids)
        
        # +1 to correct 0 based sequence
        original_name = str(sequence[resid]) + '_' + str(resid+1)
        
        mutated_scores[original_name] = mut_score_pos

    return mutated_scores, initial_score


def plot_optimization(mutated_scores, initial_score, plot_inplace=True, dpi=100):
    """

    """
    if not isinstance(mutated_scores, pd.DataFrame):
        raise TypeError('The mutate_scores variable should be a pd.DataFrame object but received a '+str(type(mutated_scores)))
    else:
        pass

    try:
        relative_sc = mutated_scores - initial_score
    except Exception as e:
        raise TypeError('The values of the mutated scores dataframe and initial_score variable should be numeric. But got error: '+str(e))
    
    try:
        dpi = int(dpi)
    except Exception as e:
        raise TypeError('The value of dpi should be an integer, but got '+str(dpi)+' instead')

    # set width between 8 and 18 depending on number of positions
    # if the maximum is passed, the x axis labels will overlap
    width = np.minimum(np.maximum(int(8*mutated_scores.shape[1]/28),8),18)
    # to have 0 centered color bar get maximum value in dataset
    max_sc = np.max(np.abs(relative_sc.values))
    
    fig, ax = plt.subplots(1, 1, figsize=(width,6), dpi=dpi)

    pcm = ax.pcolormesh(mutated_scores.columns, mutated_scores.index,
                        relative_sc.values, shading='nearest',
                        norm=colors.Normalize(vmin=-max_sc, vmax=max_sc),
                        cmap='bwr')
    cb = fig.colorbar(pcm, ax=ax, extend='both')
    cb.set_label('Change in probability for target class',  fontsize=12)
    # ax.set_xticklabels(labels, rotation=45, ha='right')
    # ax.set_xticklabels(ax.get_xticks(), rotation=90)
    ax.set_xticklabels(mutated_scores.columns, rotation=90)
    
    # to try to remove warning
#     ticks_loc = mutated_scores.columns.tolist()
#     ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
#     ax.set_xticklabels([x for x in ticks_loc])
    ax.set_xlabel('Position and original amino acid')
    ax.set_ylabel('Mutation')

    # if on a notebook, plot and return nothing or it would be plot twice 
    if plot_inplace:
        plt.show()
        return None
    # for other applications select plot_inplace=False and return the figure
    else:
        return fig

def top_mutations(mutated_scores, initial_score, top_results):

    if type(top_results) != int:
        raise TypeError('top results should be an integer')
    else:
        pass

    prob_change = mutated_scores - initial_score

    top_res = pd.DataFrame(columns=["Position","Mutation","Prob_increase","Target_probability"])

    i = 0
    # initialize at max val to enter the loop
    pred_increase = 1

    while i < top_results and pred_increase > 0:
        # get column with maximum value
        position_mut = prob_change.max().idxmax()
        # get row with maximum value
        mutation = prob_change.idxmax()[position_mut]
        pred_increase = prob_change.loc[mutation, position_mut]
        prob_value = mutated_scores.loc[mutation, position_mut]
        # change it for nan so that we can look for next result
        prob_change.loc[mutation, position_mut] = np.nan
        mut_series = pd.Series({"Position": position_mut, "Mutation": mutation,
                                "Prob_increase": pred_increase, "Target_probability": prob_value})
        top_res = top_res.append(mut_series, ignore_index=True)
        i += 1

    return top_res