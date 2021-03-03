#!/bin/bash --login
set -e

# activate conda environment and let the following process take over
conda activate lmpmenv
exec "$@"

## credit to https://stackoverflow.com/questions/55123637/activate-conda-environment-in-docker and David Pugh (https://towardsdatascience.com/conda-pip-and-docker-ftw-d64fe638dc45)
