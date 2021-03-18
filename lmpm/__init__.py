"""
Protein secretion prediction
============================

lmpm is a Python module that helps protein designers
predict and improve the secretion location (cytoplasm,
transmembrane, secreted) given the sequence of a protein
of interest.

See https://github.com/Lean-Mean-Protein-Machine-Learning/LMPM
for complete documentation.
"""

from .predict import predict_loc_simple
from .predict import predict_location
from .improve_sec import optimize_sequence
from .improve_sec import plot_optimization
from .improve_sec import top_mutations
