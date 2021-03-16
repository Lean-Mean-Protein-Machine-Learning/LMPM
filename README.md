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

### Using the web app:

We have deployed our machine learning model as a web app hosted on Heroku. It is by far
the most intuitive way to use it and offers nearly all the functionality of the module. Please, 
check it out at [https://lmpm.herokuapp.com/](https://lmpm.herokuapp.com/).

Since we are using free Heroku hosting, you may reach the memory limit. An easy alternative is
running the web app locally, so that it acts as a user interface for the module. For that you
need a working [Docker installation](https://docs.docker.com/get-docker/) and running the following commands:

```sh
git clone https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM.git
cd LMPM
docker build -t lmpm_web .
docker run -d -it -p 5000:5000 --name lmpm_image lmpm_web
```

Building the docker image will take 30 seconds and about 500 Mb of disk space. Then the app will be live and perfectly functional on your browser at `http://localhost:5000/`.

### Using as a module:

Using `lmpm` as a Python module offers more versatility than the web app and facilitates integrating its functions into an automated pipeline/workflow. For that, you only need a Python environment with the lmpm dependencies (see "Dependencies" section above) installed. Optionally, you can set up a new conda environment for this module by downloading our `environment.yml` file and creating it:

```sh
# install miniconda (if required)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# download environment specification file
wget https://raw.githubusercontent.com/Lean-Mean-Protein-Machine-Learning/LMPM/main/environment.yml

# create "lmpmenv" environment from this file
conda env create -f environment.yml

# activate environment
conda activate lmpmenv
``` 

With an environment with the required dependencies, you can then install the lmpm module with:

```sh
python3 -m pip install git+https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM
```
### For developers:

For more details on how to use the module or contribute, check our [docs/get_started.md](https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM/blob/main/docs/get_started.md) file.


<!-- USAGE EXAMPLES -->
## Usage

First, import the module:
  ```python
  import lmpm
  ```

Alternatively, the six main functions can be imported individually:
```python
from lmpm import predict_loc_simple
from lmpm import predict_location
from lmpm import optimize_sequence
from lmpm import plot_optimization
from lmpm import top_mutations
```

### Predict protein localization
The localization probability of the protein (according to the model) can be predicted using `predict_loc_simple`. The function needs the user to specify a sequence, the desired organism, and the localization of interest (secreted, membrane, or cytoplasm):
  ```python
  sequence = 'MKPNIIFVLSLLLILEKQAAVMGQKGGSKGRLPSEFSQFPHGQKGQHYSG'
  organism = 'human'
  target_location = 'secreted'
  predicted_class, secretion_score = predict_loc_simple(sequence, organism, target_location, include_dg=False)
  ```
The localization and probabilities of the protein can also be predicted using the more versatile function `predict_location`. This can be expanded to all organisms and returns the results as a class with multiple attributes:
  ```python
  sequence = 'MKPNIIFVLSLLLILEKQAAVMGQKGGSKGRLPSEFSQFPHGQKGQHYSG'
  organism = 'human'
  target_location = 'all'
  predictions = predict_location(sequence, organism, target_location, include_dg=False)
  predictions.result
  ```

### Make point mutations in sequence to improve desired localization
Point mutations can be introduced in a sequence to investigate their effects on protein localization. First, the `optimize_sequence` function takes in the sequence, organism, desired localization, and the positions for desired point mutations. Note that only one point mutation occurs at a time. The `mutated_scores` variable below returns a data frame of amino acids vs. the locations for point mutations and the values of the localization scores (as the probability of the protein belonging to the desired localization class).
  ```python
  sequence = 'MKPNIIFVLSLLLILEKQAAVMGQKGGSKGRLPSEFSQFPHGQKGQHYSG'
  organism = 'human'
  target_location = 'cytoplasm'
  positions = '4,9'
  mutated_scores, initial_score = optimize_sequence(sequence, organism, target_location, include_dg=False, positions=positions)
  ```
The outputs of this function can be represented using the `plot_optimization` function. This takes as inputs the results returned by the `optimize_sequence` function:
  ```python
  plot_optimization(mutated_scores, initial_score, plot_inplace=True, dpi=100)
  ```
Finally, the `top_mutations` function takes the results from the `optimize_sequence` function and returns the top mutations that change the localization score. The example below shows the top 10 results from the optimization function:
  ```python
  top_mutations(mutated_scores, initial_score, top_results=10)
  ```
A more informative demo notebook is available under [docs/lmpm_demo.ipynb](https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM/blob/main/docs/lmpm_demo.ipynb)

<!-- LICENSE -->
## License
This project is licensed under the MIT license.


<!-- CONTRIBUTE -->
## Contribute
Lean, Mean, Protein Machine is a completely functional module but can offer much more.

- If you have an idea and want to implement it, clone our repo and initite a pull request.
- If you find any issue using our module, open a Github issue [here](https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM/issues), we will try to fix it.
- Finally, if you like the project and would like to contribute but don't have a specific idea in mind, contact us! We have many ideas in mind on how the project could advance and about new functions that could be added to extend its functionality.

<!-- CONTACT -->
## Contact

- Melissa Ling - mling13@uw.edu Github: mling13
- Marc Exposit - mexposit@uw.edu Github: marcexpositg
- Andrew Favor - afavor@uw.edu Github: andrewfavor95
- Joe Henthorn - JosefH1@uw.edu  GitHub: JoeHenthorn
- Gizem Gokce - gizemg@uw.edu Github: gizemgokce

