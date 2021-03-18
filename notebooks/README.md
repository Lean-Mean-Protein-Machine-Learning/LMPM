All notebooks in this folder are drafts to show how we processed the data and trained the models.

Notebook reference:

Related to data:
- uniprot_access_notes.md: drafts of searches to uniprot database.
- UniProt_refined_query.ipynb: scripts used to download data into `.pkl` files. They are too large for github so they were kept in a google drive and downloaded manually into the `UniRep_datasets` folder for model training.
- regression_test.ipynb: loads datasets and shows that the classes can be identified in a PCA plot.

Related to models:
- additional_features_data_exploration.ipynb: compares the models adding additional features and shows the plots on the distribution of those features across each type of localization.
- models.ipynb: notebook used to train the final models that were used in the module.
- sklearn_supervised_models_opt_*.ipynb: set of notebooks (one for yeast, other for ecoli and another for human) to train classifiers based on sklearn. We tested multiple parameters for each classifier and used AUC as the metric to select the best. The models shown here were not finally used, it was just to check the importance of the parameters and find the best ones. Hence, these notebooks might be a bit messy, as they are a draft.
- model_load_test.ipynb: shows how to recover a `sklearn` model kept in `.pkl` format

Related to the module:
- check_inputs.ipnyb: used to create the `check_inputs.py` file of the module.
- predict_function_demonstration.ipynb: organized notebook that shows how to use the `predict_location` function of the module.
- improving_secretion_score.ipynb: draft notebook helpful in creating the `optimize_sequence.py` file of the module.
