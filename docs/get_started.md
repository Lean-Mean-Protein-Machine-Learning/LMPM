# Getting started with LMPM

## For users:

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

## For developers:

### Quick start guide

This is a quick start guide. See steps below for more details on each of them.

1. Clone the repo if you haven't done so:

```
https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM.git
```

2. Move inside the repo:

```
cd LMPM
```

3. Install the environment that includes jupyter notebook:

```
conda env create -f notebooks/environment_dev.yml
```

4. Load the environment and open jupyter notebook:

```
conda activate lmpmdev
jupyter notebook
```

You can start coding in the /notebooks folder now to develop new functions.

5. Use the `lmpm` module inside the notebook:

To import the `lmpm` module, an easy and elegant way is installing it from the
github repository (even if we have a local copy installed). For that, activate
the environment you are working with and install with pip:

```
conda activate lmpmdev
python3 -m pip install git+https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM
```

If this was successful you should now be able to see the information about this package:

```
pip show lmpm
```

Then, you can use it in your notebook as you would use any other module. Note that `unirep` is a submodule of `lmpm`.

```
from lmpm import localization_score
from lmpm import optimize_secretion
from lmpm.unirep import get_UniReps
```

**Downside:** If you make any changes to the package and want to apply the changes, you first need to push the changes to github, and reinstall the library again. This is actually not such a bad idea, as you will always be testing the module just like the final user will do.

```
# update repo first
git add (add files modified here)
git commit -m "changes description"
git push -u origin main
# now, in the environment you are using, update the lmpm package
python3 -m pip install lmpm --upgrade
```

See below for more details on each step.
### 1. Clone the repository

First, clone the github repository for the project by running:

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

From now on, every time you make a change, you will need to upload the changes in the github repo so that we keep them up to date. For instance, if I had modified a `hello.py` file, I could use:

```
git add hello.py
# always use git status to see the changes you made but not commited (if there are some, in red) and the changes you will commit (green)
git status
git commit -m "modified hello.py to etc"
git push origin main
```

*Note: If you have modified multiple files and want to commit all changes, you can also use `git add .` to commit all changes in all files.*

### 2. Prepare the environment

To avoid any dependency conflicts it is a good idea to use the same environment. We will use conda to manage environments. Try to avoid installing any package using `pip` because `conda` and `pip` do not work well together if you want to create reproducible environments.

If you do not have conda installed yet, you can follow the [installation instructions to install miniconda3](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). For instance, to install it for ubuntu, use:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

We will work with **three different environments**:

- `lmpmenv`: used for deployment. Only has the packages required by our module to run (this is numpy, pandas, sci-kit learn, matplotlib, and seaborn). This environment should be lightweight so that users
that only are interested in using our module can install it and start using it easily.

- `lmpmdev`: used for development. Includes the same packages as `lmpmenv` but includes `jupyter notebook` so that we can use it to test and develop the machine learning models. This is the one to use when working with Jupyter Notebooks to create and test new functions. Its `environment.yml` file is inside the `notebooks/` folder because it is only used in development.

- `lmpmbioservices`: used ONLY to download data from uniprot. For that, we used the bioservices library to get the data from uniprot. This library does not work in Python 3.8 and is incompatible with the other environments. We solved this by creating a third environment with python 3.7 and this library. It also has numpy, pandas, matplotlib, seaborn and jupyter notebook because we use jupyter notebooks to download data. See below for more information. Its `environment.yml` file is inside the `notebooks/` folder because it is only used in development.


In summary: use `lmpmdev` whenever you need to work with jupyter notebooks, use `lmpmenv` if you work on test the final module, and use `lmpmbioservices` if you are trying to download data from uniprot.

To create these environments run:

```
conda env create -f environment.yml 
conda env create -f notebooks/environment_dev.yml
conda env create -f notebooks/environment_bioserv.yml
```

Check if you have successfully created the environments by running the following command. You should see a list with your environments including `lmpmenv`, `lmpmdev` and `lmpmbioservices`.

```
conda env list
```

Whenever you want to work using Jupyter Notebooks, activate `lmpmdev`.

```
conda activate lmpmdev
```

If you want to test the final module, use the deployment environment instead:

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

### 3. Use Jupyter Notebook

All our notebooks are inside the `/notebooks` folder. This folder should also contain all data required to train the models.

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

### 4. Run the web app for development

The web app is a dockerized application based on flask. An initial version of the web app was based on conda for the environment, but it took too much memory. The final version of the app uses `pip` to install the packages, this is why there is a `requirements.txt` file inside the `app/` folder. This is used to build the docker container. This file contains the same packages as the `lmpmenv` environment including `flask`, which is necessary to run the web app. Since the initial version of the app used conda, we kept a dockerfile (`Dockerfile_conda`) and the `environment.yml` file that was used inside the `app/` folder (although to use them they would have to be in the main folder). This could be useful if we decided to switch back to this version. The functionality is not affected by that.

For instructions on how to run the web app locally for usage, refer to the "For users:" section at the top of this document.

To run the web app in debugging mode locally, first modify the last two lines of the `app/app.py` file.

For production, get the port assigned by heroku (changes every time) and turn off debugging mode:

```
if __name__ == "__main__":
    # use this when running in the website (heroku) or as local web app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # instead, comment lines above and uncomment below  if you run it as
    # flask app to debug (specifying port explicity is important for debugging)
    # app.run(debug=True,host='0.0.0.0',port=5000)
    # app.run(debug=True)
```

For development, use a fixed port (requisite to enable debugging) and enable debbuging:

```
if __name__ == "__main__":
    # use this when running in the website (heroku) or as local web app
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)
    # instead, comment lines above and uncomment below  if you run it as
    # flask app to debug (specifying port explicity is important for debugging)
    app.run(debug=True,host='0.0.0.0',port=5000)
    app.run(debug=True)
```

Whatever you decided to use, you can run the app locally using Docker. You should have a working Docker installation. Building the image is extremely fast now (30 seconds and takes up 500Mb of space). Before, when using the base conda environment, it took minutes and 2.5Gb of space.

```
cd LMPM
docker build -t lmpm_web .
docker run -d -it -p 5000:5000 --name lmpm_image lmpm_web
```

If you are using debugging mode, and testing different versions of the app, it is very helpful to mount to that image the local folders with the `app/` and `lmpm/` files. This way, changes you make in any of the files in these folders will be reflected immediately and automatically on the web app. Before running these commands, make sure that you are using the version of `app/app.py` shown in the section above "For development, use a fixed port etc..." so that debugging is active. *Note: replace the path of the LMPM folders in the `source` tags for the absolute path of your LMPM folder, you can get it by running `pwd` once inside the LMPM folder.*

```
cd LMPM
docker build -t lmpm_devp .
docker run -d -it --name lmpm_devpimg -p 5000:5000 --mount type=bind,source=/home/$USER/LMPM/app/,target=/app/ --mount type=bind,source=/home/$USER/LMPM/lmpm/,target=/lmpm/ lmpm_devp
```

### 5. Publish changes to heroku

To publish changes to the web app, you need to add and commit changes as usual but push them to heroku:

```
git push heroku main
```

This will be as fast as building the docker image. You also require to have heroku installed and with an account with access to that app.

### 6. Running unit tests:

First you need to install `nose`:

```
conda activate lmpmdev
pip install nose
```

Then, move to the `LMPM` directory and run the `nosetest` command just as it is done below. It will run the tests made on the local version of the module, so you don't need to worry about reinstalling the module as we have to do to use it in the `jupyter notebook`. Note that running the tests takes a while, 
as it is also testing the functions that generate mutations and that take relatively long. It should take about 5 minutes on a modern computer.

```
cd LMPM
nosetests lmpm
```

## Contribute

Lean, Mean, Protein Machine is a completely functional module but can offer much more.

- If you have an idea and want to implement it, clone our repo and initite a pull request.
- If you find any issue using our module, open a Github issue [here](https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM/issues), we will try to fix it.
- Finally, if you like the project and would like to contribute but don't have a specific idea in mind, contact us! We have many ideas in mind on how the project could advance and about new functions that could be added to extend its functionality.
