"""
Write tests for the check_inputs.py functions.
"""

from lmpm import check_inputs

def test_check_string():
    # test passing a value that is not a string
    try:
        check_inputs.Check_string(4)
    except Exception as exep:
        # if it is not, it should raise a ValueERror
        assert isinstance(exep, ValueError), 'Passing a non-string input did not raise a ValueError.'

    return None