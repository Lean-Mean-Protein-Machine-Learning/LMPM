"""
Protein secretion prediction
============================

lmpm is a Python module that helps protein designers
predict and improve the secretion location (cytoplasmatic, 
transmembrane, secreted) given the sequence of a protein
of interest.

See https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM
for complete documentation.
"""

"""
Delete later:

here we load the main functions of our module
we load the function to predict secretion scores
and the one to improve the secretions
the user will have to import them with:

from lmpm import secretion_score_unirep
from lmpm import optimize_secretion

and use them like:

lmpm.secretion_score()
lmpm.optimize_secretion()

This way the user does not have to worry about the rest of helper functions.

"""
from .predict import localization_score
from .improve_sec import optimize_secretion