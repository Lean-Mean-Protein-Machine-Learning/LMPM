"""
This file contains functions to make predictions.

It takes in a sequence (dna, amino acid in 1 or 3 letter code), 
and (optionally) an organism that the user provides. Returns the probability that the protein is secreted, transmembrane or cytoplasmic.

To get a better understanding on python imports, read: https://realpython.com/absolute-vs-relative-python-imports/
"""

import os, sys
from collections import defaultdict

import numpy as np
import pandas as pd
import pickle

from .unirep import get_UniReps
from .check_inputs import check_input


# get current path to load files as relative paths later
current_wd = os.path.dirname(os.path.abspath(__file__))
# using os.path.join to avoid issues across OS using different backslash symbols
# Importing dG parameters to params_dict
params = pd.read_csv(os.path.join(current_wd,"models","Params.csv"), header=None)
lst = params[0].values
params.set_index(lst, inplace=True)
del params[0]
params_dict = defaultdict(list)
for i, row in params.iterrows():
    for position in range(1, len(row) + 1):
        params_dict[i].append(float(row.loc[position]))

# Load trained models
model_human = pickle.load(open(os.path.join(current_wd,"models","human.pkl"), 'rb'))
model_yeast = pickle.load(open(os.path.join(current_wd,"models","yeast.pkl"), 'rb'))
model_ecoli = pickle.load(open(os.path.join(current_wd,"models","ecoli.pkl"), 'rb'))




def model_organism_selection(organism, include_dg):
    """
    Imports trained model of secretion scores based on organism data set

    Args:
        organism (str): specific organism of sequence type 
                        (all, human, yeast, ecoli)
        include_dg (Boolean): specify inclusion of additional features
                                (default=False)

    Returns:
        model: trained model of secretion probabilities for organism
    """
    # Create dictionary of loaded, trained models
    # Check specification of additional features
    if include_dg:
        model_dict = {
            'human': model_human,
            'yeast': model_yeast,
            'ecoli': model_ecoli
        }
    else: 
        model_dict = {
            'human': model_human,
            'yeast': model_yeast,
            'ecoli': model_ecoli
        }

    # Access the specific organism model
    model = model_dict[organism]

    return model


def localization_score(input_seq, organism, target_class='secreted', include_dg=False):
    """
    Finds the probability of being the target class given the
    sequence based on model and UniRep representation only

    Args:
        input_seq (str): sequence entered by the user
        organism (str):  specific organism of sequence type 
                         (all, human, yeast, ecoli)
        target_class (str): class to predict the probability
                            (secreted (default), cytoplasm, or membrane)
        include_dg (Boolean): specify inclusion of additional features
                                (default=False)

    Returns:
        predicted_class (str): predicted class of sequence
                        (cytoplasm, membrane, secreted)
        target_score (float): probability of sequence being 
                            in target class
    """

    # target class should be one of the classes of the model
    if target_class not in ['secreted', 'membrane', 'cytoplasm']:
        raise ValueError('The selected probability was: "'+str(target_class)+'", but should be either secreted, membrane or cytoplasm')
    else:
        pass

    # Select the model based on the organism
    model = model_organism_selection(organism, include_dg)

    # Obtain unirep representation of sequence
    # we use the function we created in check_inputs
    sequence = check_input(input_seq)
    values = get_UniReps(sequence)[0] # do we need this [0]?
    if include_dg:
        dg = calculate_transmembrane_dg(sequence)
        dg_standardized = (dg - 2.053619) / (2.300432 ** 2)
        values.append(dg_standardized)
    values = values.reshape(1, -1)

    # Returns class of given sequence
    predicted_class = model.predict(values)[0]

    # Grab the probabilities from the model
    classes = list(model.classes_)
    prediction_probabilities = list(model.predict_proba(values)[0])

    # Returns probability of being secreted class
    target_class_score = prediction_probabilities[classes.index(target_class)]
    
    return predicted_class, target_class_score


def calculate_transmembrane_dg(seq):
    """
    Calculates the free energy of transmembrane insertion of the sequence

    Args:
        sequence (str): amino acid sequence in single-letter format

    Returns:
        transmembrane_dG (float): free energy calculation
    """
    # First, make sure the sequence is longer than 19 residues
    if len(seq) < 19:
        raise ValueError('dG cannot be computed on sequences \
                            less than 19 residues')

    # Next, check if there are any ambiguous amino acids
    # also convert to appropiate format if it was provided in 3 letter code
    sequence = check_input(seq)

    # Starts dG calculations
    dg_values = []

    # Scans the sequence for every 19-residue frame
    for j in range(len(sequence)-18):
        running_total = 0
        segment = sequence[j:j+19]
        for k, amino_acid in enumerate(segment):
            running_total += params_dict[amino_acid][k]
        dg_values.append(running_total)

    # Finds the minimum dG value
    transmembrane_dG = min(dg_values)

    return transmembrane_dG
