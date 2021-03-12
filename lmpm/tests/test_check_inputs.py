"""
Write tests for the check_inputs.py functions.
"""

from lmpm import check_inputs

def test_check_string():
    # test passing a value that is not a string
    try:
        check_inputs.check_string(4)
    except Exception as exep:
        # if it is not, it should raise a ValueError
        assert isinstance(exep, ValueError), 'Passing a non-string input did not raise a ValueError.'

    # always return None in tests
    return None


def test_raise_error_bad_char():
    # try passing some invalid characters and see if it raises an error
    try:
        check_inputs.raise_error_bad_char('ZZ')
    except Exception as exep:
        assert isinstance(exep, AssertionError), 'Passing invalid characters did not raise an AssertionError.'
        print(exep)

    return None