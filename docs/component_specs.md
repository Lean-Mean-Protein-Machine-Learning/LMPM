# Components

1. check_sequence_input
    - Function: Check if the input sequence is valid and adapt it from different accepted formats to the format used to process data.
    - Inputs: Amino acid sequence of interest in single-letter format (str)
    - Outputs: If the sequence contain any non-standard characters, the user is prompted to enter a new sequence.
    - Dependencies: N/A
2. ambiguous_amino_acids
    - Function: Raises an error for ambiguous amino acids (X, B, and U)
    - Inputs: Amino acid sequence of interest in single-letter format (str)
    - Outputs: If the sequence contains ambiguous amino acids, returns a ValueError.
    - Dependencies: N/A
3. get_UniReps
    - Function: Converts an amino acid sequence to a set of 1900 vectors
    - Inputs: Amino acid sequence of interest in single-letter format (str)
    - Output: Array of 1900 vector float numbers
    - Dependencies: jax-unirep, unirep_utils
4. model_organism_selection
    - Function: Imports trained model of secretion scores based on organism data set and UniRep features
    - Inputs: Organism (all, human, yeast, ecoli) specified by user (str)
    - Output: Trained model of secretion scores
    - Dependencies: scikit-learn
5. secretion_score_unirep
    - Function: Finds the secretion probability of given sequence based on model and UniRep representation only
    - Inputs: Amino acid sequence (str), organism (str)
    - Outputs: Predicted localization class (str) and secretion score (float) of given amino acid sequence
    - Dependencies: unirep_utils
6. calculate_transmembrane_dG
    - Function: Calculates the free energy of transmembrane insertion of the sequence
    - Inputs: Amino acid sequence in single-letter format (str)
    - Outputs: Transmembrane free energy calculation (float)
    - Dependencies: N/A
7. secretion_optimization_unirep
    - Function: Introduces amino acid point mutation at given position to improve secretion score
    - Inputs: Amino acid sequence (str), organism (str), and desired position of point mutations (int)
    - Outputs: Mutated sequence (str), dictionary of point mutation amino acid and secretion score (dict)