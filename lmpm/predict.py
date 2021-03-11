"""
This file contains functions to make predictions.

It takes in a sequence (dna, amino acid in 1 or 3 letter code), 
and (optionally) an organism that the user provides. Returns the probability that the protein is secreted, transmembrane or cytoplasmic.

To get a better understanding on python imports, read: https://realpython.com/absolute-vs-relative-python-imports/
"""

import sys

import numpy as np
import pandas as pd
# will also require import sklearn or certain functions of sklearn

# here we import unirep as a submodule
from unirep.unirep_utils import get_UniReps

# import the function to load the sequence 
# that was defined on check_inputs.py
from .check_inputs import get_input_seq



# Importing dG parameters to params_dict
params = pd.read_csv('../notebooks/Params.csv', header=None)
lst = params[0].values
params.set_index(lst, inplace=True)
del params[0]
params_dict = defaultdict(list)
for i, row in params.iterrows():
    for position in range(1, len(row) + 1):
        params_dict[i].append(float(row.loc[position]))

    # Load trained models
    model_human = pickle.load((open('../trained_models/model_human')))
    model_yeast = pickle.load((open('../trained_models/model_yeast')))
    model_ecoli = pickle.load((open('../trained_models/model_ecoli')))




def model_organism_selection(organism):
    """
    Imports trained model of secretion scores based on organism data set

    Args:
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)

    Returns:
        model: trained model of secretion probabilities for organism
    """
    # Create dictionary of loaded, trained models
    model_dict = {
        'human': model_human,
        'yeast': model_yeast,
        'ecoli': model_ecoli
    }

    # Access the specific organism model
    model = model_dict(organism)

    return model


def secretion_score_unirep(input_seq, organism):
    """
    Finds the secretion probability of given sequence based on model
    and UniRep representation only

    Args:
        input_seq (str): sequence entered by the user
        organism (str):  specific organism of sequence type 
                         (all, human, yeast, ecoli)

    Returns:
        predicted_class (str): predicted class of sequence
                        (cytoplasm, membrane, secreted)
        secretion_score (float): probability of sequence being 
                                    in secreted class
    """
    # Select the model based on the organism
    model = model_organism_selection(organism)

    # Obtain unirep representation of sequence
    # we use the function we created in check_inputs
    sequence = get_input_seq(input_seq)
    unirep_values = get_uniReps(sequence)[0] # do we need this [0]?
    unirep_values = unirep_values.reshape(1, -1)

    # Returns class of given sequence
    predicted_class = model.predict(unirep_values)

    # Grab the probabilities from the model
    classes = list(model.classes_)
    prediction_probabilities = list(model.predict_proba(unirep_values)[0])

    # Returns probability of being secreted class
    secretion_score = prediction_probabilities[classes.index('secreted')]
    
    return predicted_class, secretion_score


def calculate_transmembrane_dg(sequence):
    """
    Calculates the free energy of transmembrane insertion of the sequence

    Args:
        sequence (str): amino acid sequence in single-letter format

    Returns:
        transmembrane_dG (float): free energy calculation
    """
    # First, make sure the sequence is longer than 19 residues
    if sequence < 19:
        raise ValueError('dG cannot be computed on sequences \
                            less than 19 residues')

    # Next, check if there are any ambiguous amino acids
    ambiguous_amino_acids(sequence)

    # Starts dG calculations
    dg_values = []

    # Scans the sequence for every 19-residue frame
    for j in range(len(sequence)-18):
        running_total = 0
        segment = sequence(j:j+19)
        for k, amino_acid in enumerate(segment):
            running_total += params_dict[amino_acid][k]
        dg_values.append(running_total)

    # Finds the minimum dG value
    transmembrane_dG = min(dg_values)

    return transmembrane_dG
