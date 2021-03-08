# Getting started with LMPM

## For users

Here we will write instructions on how to use the module to make predictions for a protein of interest. We will do so when the module is finished.


## For developers

### Brief summary HERE - if you want to start working on this fast, read this and forget about the rest

1. Clone the repo if you haven't done so:

```
https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM.git
```

2. Move inside the repo:

```
cd LMPM
```

3. Install the environment with jupyter notebook:

```
conda env create -f environment_dev.yml
```

4. Load the environment and open jupyter notebook:

```
conda activate lmpmdev
jupyter notebook
```

You can start coding in the /notebooks folder now.

If you have any problem, read in detail the steps below.


### 1. Clone the repository

If you still have not done so, clone the github repository for the project by running:

```
## if you use HTTP (default)
https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM.git
## If you use SSH
git@github.com:Lean-Mean-Protein-Machine-Learning/LMPM.git
```

And move inside the folder for the repository:

```
cd LMPM
```

If you have already cloned the repository, before starting to work on it pull the new changes:

```
git pull
```

From now on, every time you make a change, you will need to upload the changes in the github repo so that we keep them up to date. For instance, if I had modified the `hello.py` file, I could use:

```
git add hello.py
# always use git status to see the changes you made but not commited (if there are some, in red) and the changes you will commit (green)
git status
git commit -m "modified hello.py to etc"
git push origin main
```

*Note: If you have modified multiple files and want to commit all changes, you can also use `git add .` to commit all changes in all files.*

### 2. Prepare the environment

To avoid any dependency conflicts it is a good idea if we all use the same environment. We will use conda to manage environments. Try to avoid installing any package using `pip` because `conda` and `pip` do not work well together if you want to create reproducible environments.

If you do not have conda installed yet, you can follow the [installation instructions to install miniconda3](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). For instance, to install it for ubuntu, use:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

We will work with **three different environments**:

- `lmpmenv`: used for deployment. Only has the packages required by our module to run (this is numpy, sci-kit learn, matplotlib, seaborn, numba, biopython and flask). This environment should be lightweight so that it can be used efficiently on the webapp. Right now it does not have `tensorflow` nor `jupyternotebook`. If we end up using any `tensorflow` function, we can install it in this environment too.

- `lmpmdev`: used for development. This is the package we should use to test and develop the machine learning models. We shoud use this one when working with Jupyter Notebooks to create and test new functions. In addition to the packages already in `lmpmenv`, it includes `jupyter notebook`.

- `lmpmbioservices`: used to download data from uniprot ONLY. Andrew used the bioservices library to get the data from uniprot. This library does not work in Python 3.8 and is incompatible with the other environments. We solved this by creating a third environment with python 3.7 and this library. It also has numpy, pandas, matplotlib, seaborn and jupyter notebook because we use jupyter notebooks to download data. See below for more information.


In summary: use `lmpmdev` whenever you need to work with jupyter notebooks, use `lmpmenv` if you work on test the final module or the web app, and use `lmpmbioservices` if you are trying to download data from uniprot.

To create these environments run:

```
conda env create -f environment.yml 
conda env create -f environment_dev.yml
conda env create -f environment_bioserv.yml
```

Check if you have successfully created the environments by running the following command. You should see a list with your environments including `lmpmenv`, `lmpmdev` and `lmpmbioservices`.

```
conda env list
```

Whenever you want to work using Jupyter Notebooks, activate `lmpmdev`.

```
conda activate lmpmdev
```

If you want to test the web app, use the deployment environment instead:

```
conda activate lmpmenv
```

If you want to download sequences from Uniprot, use `lmpmbioservices` (but remember to switch to `lmpmdev` to train machine learning models):

```
conda activate lmpmbioservices
``` 

Whenever you want to finish working with that environments, run:

```
conda deactivate
```

**Tensorflow (optional):**

It seems that tensorflow is only supported on CPUs in Mac (https://docs.anaconda.com/anaconda/user-guide/tasks/tensorflow/). If you want to install it (optional):

First activate the development environment

```
conda activate lmpmdev
```

Then, if you want to install the CPU version (runs on Mac, Windows and Linux):

```
conda install tensorflow
```

If you want to install the GPU version (only works on Windows and Linux):

```
conda install tensorflow-gpu
```


### 3. Run Jupyter Notebook

All our notebooks are inside the /notebooks folder. This folder should also contain all data required to train the models.

To work with Jupyter notebook activate the development environment first:

```
conda activate lmpmdev
```

Then, start a jupyter notebook server:

```
cd /notebooks
jupyter notebook
```

And navigate to the adress in your browser.

### 4. Run the web app

We should stil not focus on that part of the project yet since we first should complete our python module.

#### Run the app locally

TODO: run it with docker build instead of flask

You should work with the deployment environment, so:

```
conda activate lmpmenv
```

Then, start a flask server:

```
python app/app.py
```

You will need to make sure that app.py has the correct imports and the `__init__` function the correct port. See the comments in `app.py` for more information.

#### Publish changes to heroku

To publish changes to the web app, you need to add and commit changes as usual but push them to heroku:

```
git push heroku main
```

This will take a few minutes to build the docker image and push it. You may also require to have heroku installed and with an account with access to that app.
