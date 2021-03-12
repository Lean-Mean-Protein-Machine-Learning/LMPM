"""
Write tests for the predict.py functions.
"""

from lmpm import predict


# define random sequence for testing
sequence = 'GALRNDTGALMFWK'

def test_localization_score():
    # test passing a value for target_class that is not secreted, membrane or cytoplasm
    try:
        predict.localization_score(sequence, 'ecoli', 'not_a_valid_class_for_model')
    except Exception as exep:
        # if it is not, it should raise a ValueError
        assert isinstance(exep, ValueError), 'Passing a class that is not secreted, membrane, or cytoplasm did not raise a ValueError'

    return None
