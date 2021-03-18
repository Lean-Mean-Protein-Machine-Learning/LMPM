#!/bin/bash --login
set -e

# this file was required when using the conda environment for the web app. This was slow and took too much memory, so it is no longer needed.

# activate conda environment and let the following process take over
conda activate lmpmenv
exec "$@"

## credit to https://stackoverflow.com/questions/55123637/activate-conda-environment-in-docker and David Pugh (https://towardsdatascience.com/conda-pip-and-docker-ftw-d64fe638dc45)
