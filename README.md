# Lean Mean Protein Machine (Learning)
* Andrew Favor
* Melissa Ling
* Joe Henthorn
* Marc Expòsit
* Gizem Gokce

# Project Overview
Structure-based design of proteins is promising in synthetic biology research. This has many applications, such as development of nanoparticle vaccines. However, one of the major hurdles to function and use of designed nanoparticles is sub-optimal secretion. In this project, we will analyze native, characterized proteins in the human proteome in order to understand what features contribute to protein secretion (such as isoelectric point, amino acid length, and protein size). We will develop a model that can predict whether a designed protein will be secreted out of the cell, become a transmembrane protein, or remain a soluble or intracellular protein.

# Dependencies
1. [BioPython](https://anaconda.org/bioconda/biopython)
	- Tools for computational molecular biology, including sequence conversion utilities
2. [Pandas](https://anaconda.org/anaconda/pandas)
	- Data-organization framework
3. [Numpy](https://anaconda.org/anaconda/numpy)
	- Numerical operations
4. [Scikit-Learn](https://anaconda.org/anaconda/scikit-learn)
    - Supervised machine learning models
5. [Biopython](https://anaconda.org/anaconda/biopython)
    - Set of biological functions for protein analysis
6. [Jax](https://anaconda.org/conda-forge/jax)
	- High-efficiency math library, optimized for accelerated linear algebra (XLA)
7. [Jax-UniRep](https://github.com/ElArkk/jax-unirep)
	- Library for applying the protein sequence-encoding paradigm, [UniRep](https://www.nature.com/articles/s41592-019-0598-1), implemented using Jax instead of Tensorflow
