# Lean Mean Protein Machine!

[![Build Status](https://travis-ci.com/Lean-Mean-Protein-Machine-Learning/LMPM.svg?branch=main)](https://travis-ci.com/Lean-Mean-Protein-Machine-Learning/LMPM)
[![Coverage Status](https://coveralls.io/repos/github/Lean-Mean-Protein-Machine-Learning/LMPM/badge.svg?branch=main)](https://coveralls.io/github/Lean-Mean-Protein-Machine-Learning/LMPM?branch=main)

<img src='img/LMPM_logo.png' width=250px>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#project-overview">Project Overview</a></li>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Project Overview

Structure-based design of proteins shows great promise in nanoparticle vaccines. However, one of the major hurdles to function and use of designed nanoparticles is sub-optimal secretion. In this project, we have analyzed proteins in three different organisms (humans, yeast, and E. Coli) to correlate subcellular location to genetically encodable features. We have also added an option of extending this model to include transmembrane potential, percent of secondary structure helices, and flexibility of amino acids. These models predict the probability of a protein being in the secreted class. We have also added a function to introduce point mutations into a designed protein to improve the secretion score.

## Dependencies
1. [Pandas](https://anaconda.org/anaconda/pandas)
	- Data-organization framework
2. [Numpy](https://anaconda.org/anaconda/numpy)
	- Numerical operations
3. [Scikit-Learn](https://anaconda.org/anaconda/scikit-learn)
    - Supervised machine learning models
4. [Matplotlib](https://anaconda.org/anaconda/matplotlib)
	- Data Visualization in python 
5. [Seaborn](https://anaconda.org/anaconda/seaborn)
	- High-level interface for attractive graphics


<!-- GETTING STARTED -->
## Getting Started



Clone the repository:

  ```sh
  https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM.git
  ```
Move inside the repository:

  ```sh
  cd LMPM
  ```
Install the environment:

  ```sh
  conda env create -f environment_dev.yml
  ```
Load the environment and open jupyter notebook:

  ```sh
  conda activate lmpmdev
  jupyter notebook
  ```


<!-- USAGE EXAMPLES -->
## Usage

First, import functions:
  ```python
  from lmpm import improve_sec, predict
  ```
### Predict secretion score
The secretion score of a protein can be predicted from our trained models with `secretion_score`. See an example below:
  ```python
  sequence = 'MKPNIIFVLSLLLILEKQAAVMGQKGGSKGRLPSEFSQFPHGQKGQHYSG'
  organism = 'human'
  predicted_class, secretion_score = secretion_score(sequence, organism)
  ```
### Make point mutations in sequence to improve secretion score
Point mutations can be introduced in a sequence to improve secretion score. This can be done using our trained models with `secretion_optimization`. See an example below:
  ```python
  sequence = 'MKPNIIFVLSLLLILEKQAAVMGQKGGSKGRLPSEFSQFPHGQKGQHYSG'
  organism = 'human'
  position = 10
  mutated_sequence, _ = secretion_optimization(sequence, organism, position)
  ```


<!-- LICENSE -->
## License





<!-- CONTACT -->
## Contact

- Melissa Ling - mling13@uw.edu
- Marc Exposit
- Andrew Favor
- Joe Henthorn - JosefH1@uw.edu  GitHub: JoeHenthorn
- Gizem Gokce

