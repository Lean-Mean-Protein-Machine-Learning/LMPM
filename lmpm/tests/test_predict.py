"""
Write tests for the predict.py functions.
"""

import lmpm.predict as predict

# import predict


# define random sequence for testing
sequence = 'GALRNDTGALMFWK'

# def test_localization_score():
#     # test passing a value for target_class that is not secreted, membrane or cytoplasm
#     try:
#         predict.localization_score(sequence, 'ecoli', 'not_a_valid_class_for_model')
#     except Exception as exep:
#         # if it is not, it should raise a ValueError
#         assert isinstance(exep, ValueError), 'Passing a class that is not secreted, membrane, or cytoplasm did not raise a ValueError'

#     return None


def test_model_organism_selection():
    organism = ['all', 'human', 'yeast', 'ecoli', 'space aliens']
    include_dg = [False, True, '']

    for lifeform in organism:
        for DG in include_dg:
            try:
                predict.model_organism_selection(lifeform, DG)
            except Exception as exep:
                assert isinstance(exep, ValueError), "Issue in test_model_organism_selection()"

# 	predict.model_organism_selection(organism, include_dg)



def test_calculate_transmembrane_dg():
	
    seq1 = 'AAAAAAAAAAAAA' #13 AA's 
    seq2 = 'AAAAAAAAAAAAAAAAAAAA' # 20 AA's

    sequences = [seq1, seq2]

    for seq in sequences:
	    try:
		    predict.calculate_transmembrane_dg(seq)
	    except Exception as exep:
			# if it is not, it should raise a ValueError
	        assert isinstance(exep, ValueError), 'dG cannot be computed on sequences less than 19 residues'


def test_predict_loc_simple():
    input_seq = 'GALRNDTGALMFWK'
    organism = ['human', 'yeast', 'ecoli', 'space aliens']
    target_loc = ['secreted', 'membrane', 'cytoplasm', 'Zeta Reticuli']
    include_dg  = [False, True, '']

    for lifeform in organism:
        for DG in include_dg:
            for fate in target_loc:
                try:
                    predict.predict_loc_simple(input_seq, lifeform, fate, DG)
                except Exception as exep:
					# if it is not, it should raise a ValueError
                    assert isinstance(exep, ValueError), ("Passing an correct target location of " + fate + 
	        												" caused an error.")


def test_predict_location():
    input_seq = 'GALRNDTGALMFWK'
    organism = ['human', 'yeast', 'ecoli', 'space aliens']
    target_loc = ['all', 'secreted', 'membrane', 'cytoplasm', 'Zeta Reticuli']
    include_dg = [False, True, '']
    pred_all = [False, True, '']

    for lifeform in organism:
        for DG in include_dg:
            for fate in target_loc:
                for pred in pred_all:
                    try:
                        predict.predict_location(input_seq, lifeform, fate, DG, pred)
                    except Exception as exep:
                        # if it is not, it should raise a ValueError
                        assert isinstance(exep, ValueError), ("Passing an correct target location of " + fate + 
		        												" caused an error.")




