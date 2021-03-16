# Use cases
1. Provide and check the sequence(s) of interest.
	- Protein designer/researcher provides the sequence of one or multiple proteins, as amino acid sequence(s) in single- or three-letter format.
	- System detects the input format and looks for non-standard characters for protein sequences.
	- If the input has any non-standard character or any ambiguous amino acids (e.g. X, B, U), returns an error and promps the user for a correct sequence. If the input is correct, the system proceeds.
2. Convert the input sequence to a single-letter amino acid sequence (*implicit*).
	- System takes the input provided by the user in any of the possibile formats and converts it to a singe-letter amino acid sequence.  
3. Standardizing amino acid sequence through UniRep (*implicit*).
	- System implicitly uses UniRep to featurize the amino acid sequences to a 1900-element vector.
4. Select organism and trained model.
    - Protein designer/researcher provides the organism of the protein sequence of interest. This can be: all, human, yeast, or E. coli.
5. Predict secretion/cytoplasmic/membrane score with UniRep features.
	- System enters the sequence-based vector into a pre-trained model and returns a secretion/cytoplasmic/membrane score.
	- The protein designer/researcher gets the secretion/cytoplasmic/membrane score for each of the sequences provided as input.
6. Optimize secretion/cytoplasmic/membrane score accuracy with additional features.
	- Researcher choosed to add additional features: theoretical free energy of transmembrane insertion, flexibility, percent beta sheets.
	- Model returns an improved score based on additional features.
7. Improve the secretion/cytoplasmic/membrane score of a protein of interest.
	- Protein designer has the option to improve the score of the protein of interest.
	- If the user selects this option, the model uses site saturation mutagenesis or a genetic algorithm to generate diversity from the initial sequence of interest.
    - Protein designer provides the amino acid sequence, the desired position for point mutations, and the organism.
	- This newly generated sequences are analyzed in batch with the model to identify mutations that could increase the predicted score of the protein.
	- The protein designer visualizes the results and uses that information to improve the score of the protein of interest.