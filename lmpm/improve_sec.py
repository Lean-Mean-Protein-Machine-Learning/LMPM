"""
The scripts in this file help improve the localization scores for a sequence.

The main function takes in a sequence, the target localization (cytoplasmic/
transmembrane/secreted), a target organism and a set of positions to mutate.

The function mutates each position for all possible amino acids and evaluates
the probability that the mutated sequence is localized at the target location.
Other functions help representing the results and getting a list of the
best mutations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

from .check_inputs import check_input
from .predict import predict_loc_simple

amino_acids = [
    "G",
    "A",
    "L",
    "M",
    "F",
    "W",
    "K",
    "Q",
    "E",
    "S",
    "P",
    "V",
    "I",
    "C",
    "Y",
    "H",
    "R",
    "N",
    "D",
    "T",
]


def get_residue_positions(positions):
    """Converts a list of integers or ranges to individual residue numbers.

    This function is used to process the input string for the positions to
    mutate. It takes in a string of integers representing residue positions.
    This string must be a list of comma-separated integers. Ranges can also
    be defined using "-" between two integers.
    Note1: The ranges are INCLUSIVE.
    Note2: The positions in the sequence are 1-based (not zero-based), so
        the first residue of the protein is residue number 1.

    Args:
        positions: string with a list of protein residues.
            Example: "1,3-5,8,10-12"

    Returns:
        res_posit: list of individual residues.
            Example: [1,3,4,5,8,10,11,12]
    """

    # initialize list
    res_posit = np.array([])

    # preprocess string to get list of integers or ranges
    positions = positions.split(",")

    for item in positions:
        # split if element contains a "-" and is a range
        try:
            item = np.array(str(item).split("-"), dtype="int")
        # if it can't be converted to integer, raise ValueError
        except Exception as e:
            raise ValueError(
                'The position should be a list of integers or ranges '
                + 'defined as: "integer-integer", error ' + str(e)
            )

        if len(item) == 2:
            # if the element had a "-" the length will be 2 (initial-final pos)
            # create a range of integers from lower to higher value
            res_posit = np.append(res_posit, list(range(item[0], item[1] + 1)))
        elif len(item) == 1:
            # if it only had an integer, append this integer to the list
            res_posit = np.append(res_posit, item)

    # convert to numpy array and make sure all are integers
    # no need to raise ValueError because that was previously checked
    res_posit = np.array(np.unique(np.sort(res_posit)), dtype="int")

    return res_posit


def optimize_sequence(
    seq, organism, target_class, include_dg=False, positions=None
):
    """Predicts the effect on localization of mutations at selected positions.

    This function takes in an amino acid sequence, a target localization and
    organism, a True/False value on whether to include extra features (deltaG)
    and (optionally) a list of positions to mutate. All positions are
    considered if no list of positions is passed in.
    The function mutates all positions of the sequence and uses the ML model
    to predict the probability that the protein is localized at the target
    localization for the given organism.
    Note that the number of sequences tested increases rapidly with the number
    of positions, as 20 amino acids have to be tested for each position
    (20*num_positions). It only looks at single-site mutations, if not the
    amount of testing would increase even further (20^numb_positions).
    With the current implementation there is a limit at 10 total positions to
    mutate to avoid spending too much time computing the results. However,
    users could run the function in parallel to get results for all positions.

    Args:
        seq: string with the amino acid sequence
        organism: either human, yeast or ecoli
        target_class: either cytoplasm, membrane or secreted
        include_dg: whether to include delta G to the model (True/False)
        positions: a string indicating the positions to mutate e.g "1,3-5,8"

    Returns:
        mutated_scores: a pd.DataFrame with columns indicating the position and
            original amino acid and rows for all different amino acids tested
            at that position. Cells contain the probability of the mutated
            sequence of being localized at the target localization.
        initial_score: the probability of being secreted to the target
            localization for the original sequence
    """
    # First, check if there are any ambiguous amino acids or invalid symbols
    # and convert to appropiate format if it was provided in 3 letter code
    sequence = check_input(seq)

    # Then, find the predicted localization and initial score for this local.
    initial_score = predict_loc_simple(
        sequence, organism, target_class, include_dg
    )

    if positions is None:
        # if no position was specified, mutate all
        res_poses = np.array(list(range(0, len(sequence))))
    else:
        # if positions were specified, convert to list with previous function
        res_poses = get_residue_positions(positions)
        # convert positions to 0 based positions for ease of working in python
        res_poses = res_poses - 1

        # check if the largest position value is within the protein length
        if np.max(res_poses) + 1 > len(sequence):
            raise ValueError(
                "You passed residue position "
                + str(np.max(res_poses) + 1)
                + ", which is larger than the protein length of "
                + str(len(sequence))
                + " residues."
            )
        else:
            pass

    # converting to unirep can be slow for long sequences
    # since this function requires evaluating 20*(numb. positions) sequences
    # we will limit the number of positions to mutate to 10
    # Future developments to remove this limit could be:
    #    - use numba to speed up unirep (easy because it is numpy implemented)
    #    - estimate time it takes depending on protein lenght, inform the user
    #      and let the user decide if the process should be done or not
    if len(res_poses) > 10:
        raise ValueError(
            "The maximum number of residues to mutate is currently set at 10. "
            + "Going over this maximum would take too much time with the "
            + "current implementation, sorry."
        )

    mutated_scores = pd.DataFrame()

    # for each positon to mutate
    for resid in res_poses:
        mut_score_pos = []
        # generate all possible mutations
        for mutation in amino_acids:
            mutated_seq = (
                sequence[:resid] + str(mutation) + sequence[resid + 1:]
            )
            # evaluate each of them with the machine learning model
            pred_score = predict_loc_simple(
                mutated_seq, organism, target_class, include_dg
            )
            mut_score_pos.append(pred_score)

        mut_score_pos = pd.Series(mut_score_pos, index=amino_acids)

        # get the name for the mutated position
        # +1 to correct 0 based sequence handled by function internally
        original_name = str(sequence[resid]) + "_" + str(resid + 1)
        # keep results in data frame
        mutated_scores[original_name] = mut_score_pos

    return mutated_scores, initial_score


def plot_optimization(
    mutated_scores, initial_score, plot_inplace=True, dpi=100
):
    """Represents a heatmap indicating how mutations affect localization.

    This function takes in a pd.DataFrame and an intial value, substracts the
    initial value to each value in the pd.DataFrame and represents a heatmap
    showing the differences between the values in the pd.DataFrame and the
    initial value. Higher (positive) values are shown in red and lower
    (negative) values in blue. The color scale is symmetric and adjusted to the
    maximum absolute value of differences.

    In this context, the heatmap takes in the pd.DataFrame of scores for each
    mutation and the probability of being secreted at the target location for
    the initial sequence without mutations. The heatmap then represents how
    much each mutation at each position increases (red) or decreases (blue) the
    probability of the protein to be localized at the target localization.

    The size of the heatmap is adjusted depending on the number of positions,
    but it is only clear if the number of positions is below 40.

    Args:
        mutated_scores: a pd.DataFrame with the probability predicted by the
            model for each mutation (rows) at each position (columns).
        initial_score: a float representing the probability predicted by the
            model for the initial sequence.
        plot_inplace: use True (default) if using the function on a Jupyter
            Notebook, so that the plot is shown and not returned. If using
            False in a Jupyter Notebook the plot will be represented twice.
            The False option returns the plot so that it can be stored in a
            variable, which was useful for the web app.
        dpi: dots per inch value of the generated figure. Defaults to 100,
            use 300 for better resolution.

    Returns:
        heatmap representation of how each mutation improves or decreases the
            probability of being localized at the target localization.
    """
    # check if input is pd.DataFrame
    if not isinstance(mutated_scores, pd.DataFrame):
        raise TypeError(
            "The mutate_scores variable should be a pd.DataFrame object "
            + "but received a "+str(type(mutated_scores))
        )
    else:
        pass

    # check if all values are numeric by attempting to substract initial_score
    try:
        relative_sc = mutated_scores - initial_score
    except Exception as e:
        raise TypeError(
            "The values of the mutated scores dataframe and initial_score"
            + "variable should be numeric. But got error: "
            + str(e)
        )

    # check if dpi is an integer value
    try:
        dpi = int(dpi)
    except Exception as e:
        raise TypeError(
            "The value of dpi should be an integer, but got "
            + str(type(dpi))
            + " instead, so the error is:" + str(e)
        )

    # set width between 8 and 18 depending on number of positions
    # if the maximum is passed, the x axis labels will overlap
    width = np.minimum(np.maximum(int(8 * mutated_scores.shape[1] / 28), 8),
                       18)
    # to have a centered color bar (white=0) get maximum value in dataset
    max_sc = np.max(np.abs(relative_sc.values))

    # determine figure shape
    fig, ax = plt.subplots(1, 1, figsize=(width, 6), dpi=dpi)

    # create color representation according to the maximum value in the data
    pcm = ax.pcolormesh(
        mutated_scores.columns,
        mutated_scores.index,
        relative_sc.values,
        shading="nearest",
        norm=colors.Normalize(vmin=-max_sc, vmax=max_sc),
        cmap="bwr",
    )
    # insert colorbar
    cb = fig.colorbar(pcm, ax=ax, extend="both")
    # label
    cb.set_label("Change in probability for target class", fontsize=12)
    ax.set_xticklabels(mutated_scores.columns, rotation=90)

    # to try to remove warning about xticklabels
    #     ticks_loc = mutated_scores.columns.tolist()
    #     ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
    #     ax.set_xticklabels([x for x in ticks_loc])
    ax.set_xlabel("Position and original amino acid", fontsize=12)
    ax.set_ylabel("Mutation", fontsize=12)

    # if on a notebook, plot and return nothing or it would be plot twice
    if plot_inplace:
        plt.show()
        return None
    # for other applications select plot_inplace=False and return the figure
    else:
        return fig


def top_mutations(mutated_scores, initial_score, top_results=10):
    """Generate list of n mutations that improve localization probability

    Takes in the pd.DataFrame of predictions for mutated sequences and the
    probability of the initial sequence. After substracting the initial value
    from the values of the mutations, it generates a list of the mutations
    that increase the probability that the protein is localized at the target
    localization. The number of mutations returned is determined with the
    top_results variable, which defaults to 10. Note that if there are not so
    many beneficial mutations as indicated in top_results, the returned list is
    shorter to avoid returning mutations that would decrease the probability of
    being localized at the target localization. This means that if all
    mutations are detrimental, the function returns an empty pd.DataFrame.

    The returned mutations are sorted from larger increase to smaller increase
    and include information about the amino acid position, the original
    residue at that position, the mutation, the improvement with respect to
    initial_score and the final probability of the sequence with that mutation.

    Args:
        mutated_scores: a pd.DataFrame with the probability predicted by the
            model for each mutation (rows) at each position (columns).
        initial_score: a float representing the probability predicted by the
            model for the initial sequence.
        top_results: an integer indicating the number of mutations to return.

    Returns:
        top_res: a pd.DataFrame with the mutations that improve the
            probability that a protein is localized at the target localization,
            showing position, mutation and improvement with respect to the
            original score.
    """
    # check if top_results is an integer
    if type(top_results) != int:
        raise TypeError("top results should be an integer")
    else:
        pass

    # get the increase or decrease in probability of mutations compared to the
    # initial_score of the original sequence
    prob_change = mutated_scores - initial_score

    # prepare data frame for results
    top_res = pd.DataFrame(
        columns=["Position", "Mutation", "Prob_increase", "Target_probability"]
    )

    i = 0
    # initialize at max value so that it enters the loop
    pred_increase = 1

    # get best mutations until reaching top_results or mutations that do
    # not improve the probability
    while i < top_results and pred_increase > 0:
        # get column with maximum value
        position_mut = prob_change.max().idxmax()
        # get row with maximum value
        mutation = prob_change.idxmax()[position_mut]
        # get increase and localization probability of the sequence with the
        # mutation of interest
        pred_increase = prob_change.loc[mutation, position_mut]
        prob_value = mutated_scores.loc[mutation, position_mut]
        # change it for nan so that we can look for next worse mutation at the
        # next iteration
        prob_change.loc[mutation, position_mut] = np.nan
        # append to results
        mut_series = pd.Series(
            {
                "Position": position_mut,
                "Mutation": mutation,
                "Prob_increase": pred_increase,
                "Target_probability": prob_value,
            }
        )
        top_res = top_res.append(mut_series, ignore_index=True)
        i += 1

    return top_res
