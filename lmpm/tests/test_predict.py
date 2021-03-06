"""
Write tests for the predict.py functions.
"""

import numpy as np
import pandas as pd

import lmpm.predict as predict

# define random sequence for testing
sequence = "ALIENSRCMING"


def test_model_organism_selection():
    organism = ["all", "human", "yeast", "ecoli", "space aliens"]
    include_dg = [False, True, ""]

    for lifeform in organism:
        for DG in include_dg:
            try:
                predict.model_organism_selection(lifeform, DG)
            except Exception as exep:
                assert isinstance(
                    exep, ValueError
                ), "Issue in test_model_organism_selection()"


# 	predict.model_organism_selection(organism, include_dg)


def test_calculate_transmembrane_dg():

    seq1 = "AAAAAAAAAAAAA"  # 13 AA's
    seq2 = "AAAAAAAAAAAAAAAAAAAA"  # 20 AA's

    sequences = [seq1, seq2]

    for seq in sequences:
        try:
            predict.calculate_transmembrane_dg(seq)
        except Exception as exep:
            # if it is not, it should raise a ValueError
            assert isinstance(
                exep, ValueError
            ), "dG cannot be computed on sequences less than 19 residues"


def test_predict_loc_simple():
    input_seq = "ALIENSRCMINGALIENSRCMING"
    organism = ["human", "yeast", "ecoli", "space aliens"]
    target_loc = ["secreted", "membrane", "cytoplasm", "Zeta Reticuli"]
    include_dg = [False, True, ""]

    for lifeform in organism:
        for DG in include_dg:
            for fate in target_loc:
                try:
                    predict.predict_loc_simple(input_seq, lifeform, fate, DG)
                except Exception as exep:
                    # if it is not, it should raise a ValueError
                    assert isinstance(exep, ValueError), (
                        "Passing an correct target location of "
                        + fate
                        + " caused an error."
                    )

    # check output
    result = predict.predict_loc_simple(
        input_seq, organism[0], target_loc[0], include_dg=True
    )
    assert isinstance(
        result, np.float64
    ), "The result of predict_loc_simple is not a np.float"


def test_predict_location():
    input_seq = "ALIENSRCMINGALIENSRCMING"
    organism = ["human", "yeast", "ecoli", "space aliens"]
    target_loc = ["all", "secreted", "membrane", "cytoplasm", "Zeta Reticuli"]
    include_dg = [False, True, ""]
    pred_all = [False, True, ""]

    for lifeform in organism:
        for DG in include_dg:
            for fate in target_loc:
                for pred in pred_all:
                    try:
                        predict.predict_location(
                            input_seq, lifeform, fate, DG, pred
                        )
                    except Exception as exep:
                        # if it is not, it should raise a ValueError
                        assert isinstance(exep, ValueError), (
                            "Passing an correct target location of "
                            + fate
                            + " caused an error."
                        )
    # check output
    result = predict.predict_location(
        input_seq, "all", target_loc[0], include_dg=True
    )
    assert isinstance(
        result(), pd.DataFrame
    ), "The result of predict_location for all organisms is not a pd.DataFrame"

    result = predict.predict_location(
        input_seq, organism[0], target_loc[1], include_dg=True
    )
    assert isinstance(
        result(), pd.Series
    ), str("The result of predict_location with defined organisms is not a"
           + "pd.Series")
