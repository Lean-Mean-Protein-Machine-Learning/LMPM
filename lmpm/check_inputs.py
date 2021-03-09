"""
This file contains functions for processing the input.

It takes in a sequence (dna, amino acid in 1 or 3 letter code),
converts it to amino acids in 1 letter code style
and reises errors if it contains unambiguous aminoacids, or other symbols that
do not correspond to any aminoacid.

To get a better understanding on python imports, read: https://realpython.com/absolute-vs-relative-python-imports/
"""


## here are two sample functions, fill it up / modify as needed

def ambiguous_amino_acids(sequence):
    """
    Helper function that returns true if there are ambiguous amino acids: X, B, and U

    Args: sequence (str): amino acid sequence in single-letter format

    Returns:
        True if sequence contains ambiguous amino acids
        False if sequence does not contain ambiguous amino acids
    """

    return None


def get_input_seq(input_sequence):
    """ Wrapper function to process the inputs

    Checks the input sequence to ensure that amino acids are in
    single-letter format, does not contain ambigouous amino acids
    or unvalid characters. If the input sequence is in 3 letter
    format it converts it to 1 letter format. May add dna conversion as well

    Args:
        input_sequence (str): input from the user

    Returns:
        Returns the amino acid sequence after checking that is correct and in 1 letter format
    """

    # transform the input and do the checks as necessary. Raise errors if needed.
    
    # check if contains ambiguous amino acids with the ambiguous_amino_acids function
    # if true, raise a ValueError.

    return sequence