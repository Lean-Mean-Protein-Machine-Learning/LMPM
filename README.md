# Lean Mean Protein Machine (Learning)

# Project Overview
Structure-based design of proteins is promising in synthetic biology research. This has many applications, such as development of nanoparticle vaccines. However, one of the major hurdles to function and use of designed nanoparticles is sub-optimal secretion. In this project, we will analyze native, characterized proteins in the human proteome in order to understand what features contribute to protein secretion (such as isoelectric point, amino acid length, and protein size). We will develop a model that can predict whether a designed protein will be secreted out of the cell, become a transmembrane protein, or remain a soluble or intracellular protein.

# Use cases
1. Standardizing amino acid sequence through UniRep.
    - Protein designer/researcher provides amino acid sequence in single-letter format.
    - System implicitly returns a 1900-element vector based on sequence.
2. Predict secretion score with UniRep features.
    - Protein designer/researcher provides amino acid sequence in single-letter format.
    - System enters the sequence-based vector into CNN (?) and returns a secretion score.
3. Optimize secretion score accuracy with additional features.
    - Researcher provides additional protein data, such as amino acid length and theoretical/experimental isoelectric point, in addition to amino acid sequence.
    - Model returns an improved secretion score based on additional features.
4. Comparison of models.
