# Lean Mean Protein Machine (Learning)
* Andrew Favor
* Melissa Ling
* Joe Henthorn
* Marc Expòsit

# Project Overview
Structure-based design of proteins is promising in synthetic biology research. This has many applications, such as development of nanoparticle vaccines. However, one of the major hurdles to function and use of designed nanoparticles is sub-optimal secretion. In this project, we will analyze native, characterized proteins in the human proteome in order to understand what features contribute to protein secretion (such as isoelectric point, amino acid length, and protein size). We will develop a model that can predict whether a designed protein will be secreted out of the cell, become a transmembrane protein, or remain a soluble or intracellular protein.

# Use cases
1. Provide and check the sequence/s of interest.
	- Protein designer/researcher provides the sequence of one or multiple proteins, either as DNA sequences in FASTA format or as amino acid sequences (in single- or three-letter format).
	- System detects the input format and looks for non-standard characters for DNA or protein sequences.
	- If the input has any non-standard character, returns an error and promps the user for a correct sequence. If the input is correct, the system proceeds.
2. Convert the input sequence to a single-letter amino acid sequence (*implicit*).
	- System takes the input provided by the user in any of the possibile formats and converts it to a singe-letter amino acid sequence.  
3. Standardizing amino acid sequence through UniRep (*implicit*).
	- System implicitly uses UniRep to featurize the amino acid sequences to a 1900-element vector.
4. Predict secretion score with UniRep features.
	- System enters the sequence-based vector into a pre-trained model and returns a secretion score.
	- The protein designer/researcher gets the secretion score for each of the sequences provided as input.
5. Optimize secretion score accuracy with additional features.
	- Researcher provides additional protein data, such as amino acid length and theoretical/experimental isoelectric point, in addition to amino acid sequence.
	- Model returns an improved secretion score based on additional features.
6. Improve the secretion of a protein of interest.
	- After receiving the results of the provided protein, the protein designer has the option to improve the secretion of te protein of interest.
	- If the user selects this option, the model uses site saturation mutagenesis or a genetic algorithm to generate diversity from the initial sequence of interest.
	- This newly generated sequences are analyzed in batch with the model to identify mutations that could increase the predicted secretion of the protein.


# Dependencies
1. [BioPython](https://anaconda.org/bioconda/biopython)
	- Tools for computational molecular biology, including sequence conversion utilities
2. [Pandas](https://anaconda.org/anaconda/pandas)
	- Data-organization framework
3. [Numpy](https://anaconda.org/anaconda/numpy)
	- Numerical operations
4. [Jax](https://anaconda.org/conda-forge/jax)
	- High-efficiency math library, optimized for accelerated linear algebra (XLA)
5. [Jax-UniRep](https://github.com/ElArkk/jax-unirep)
	- Library for applying the protein sequence-encoding paradigm, [UniRe](https://www.nature.com/articles/s41592-019-0598-1), implemented using Jax instead of Tensorflow
