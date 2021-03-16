# Components

1. `check_sequence_input`
    - Function: Check if the input sequence is valid and adapt it from different accepted formats to the format used to process data.
    - Inputs: Amino acid sequence of interest in single-letter format (str)
    - Outputs: If the sequence contain any non-standard characters, the user is prompted to enter a new sequence.
    - Dependencies: N/A
2. `ambiguous_amino_acids`
    - Function: Raises an error for ambiguous amino acids (X, B, and U)
    - Inputs: Amino acid sequence of interest in single-letter format (str)
    - Outputs: If the sequence contains ambiguous amino acids, returns a ValueError.
    - Dependencies: N/A
3. `get_UniReps`
    - Function: Converts an amino acid sequence to a set of 1900 vectors
    - Inputs: Amino acid sequence of interest in single-letter format (str)
    - Output: Array of 1900 vector float numbers
    - Dependencies: jax-unirep, unirep_utils
4. `model_organism_selection`
    - Function: Imports trained model of secretion scores based on organism data set and UniRep features
    - Inputs: Organism (human, yeast, ecoli) specified by user (str)
    - Output: Trained model of secretion scores
    - Dependencies: scikit-learn
5. `predict_loc_simple`
    - Function: Returns the probability of the given protein belonging to the desired subcellular location
    - Inputs: Organism (str), amino acid sequence (str), target localization (str)
    - Outputs: Predicted localization score (float) of given amino acid
    - Dependencies: sci-kit learn, `get_UniReps`
6. `predict_location`
    - Function: Finds probability of being the target class given the sequence and model
    - Inputs: Amino acid sequence (str), organism (str), target localization (str)
    - Outputs: predicted localization of protein, probability of sequence being in target class
    - Dependencies: `get_UniReps`, `model_organism_selection`, NumPy
7. `calculate_transmembrane_dG`
    - Function: Calculates the free energy of transmembrane insertion of the sequence
    - Inputs: Amino acid sequence in single-letter format (str)
    - Outputs: Transmembrane free energy calculation (float)
    - Dependencies: NumPy
8. `get_residue_positions`
    - Function: Converts a list of integers or ranges of residues into individual residue numbers
    - Inputs: Positions in str format (e.g. 1-5,8)
    - Outputs: List of individual residue positions
    - Dependencies: NumPy
9. `optimize_sequence`
    - Function: Returns the initial localization score and the mutated localization scores after point mutations at given residue positions
    - Inputs: Amino acid sequence (str), organism (str), target localization class (str), positions (str)
    - Outputs: Initial localization score (float) and mutated localization scores for each position (DataFrame)
    - Dependencies: NumPy, Pandas, `predict_loc_simple`
10. `plot_optimization`
    - Function: Plots the localization score of the point mutations of each amino acid at each given position as a heatmap with numbers relative to the initial score
    - Inputs: Mutated scores (DataFrame), initial score (float), both from the optimize_sequence function
    - Outputs: Heatmap of localization scores
    - Dependencies: NumPy, Pandas, `optimize_sequence`
11. `top_mutations`
    - Function: Takes the output of the `optimize_sequence` function and returns the top mutations that change the localization score
    - Inputs: Mutated scores (DataFrame), initial score (float), both from the `optimize_sequence` function; number of desired top results (int)
    - Outputs: Top results (DataFrame)
    - Dependencies: Pandas, `optimize_sequence`