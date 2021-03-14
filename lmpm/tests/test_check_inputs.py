"""
Write tests for the check_inputs.py functions.

"""

import lmpm.check_inputs as check_inputs

# def test_check_string():
#     # test passing a value that is not a string
#     try:
#         check_inputs.check_string(4)
#     except Exception as exep:
#         # if it is not, it should raise a ValueError
#         assert isinstance(exep, ValueError), 'Passing a non-string input did not raise a ValueError.'

#     # always return None in tests
#     return None

def test_check_string():
    # test passing a value that is not a string
    try:
        check_inputs.check_string(4)
    except Exception as exep:
        assert isinstance(exep, AssertionError), "An unplanned error occured. Not an 'AssertionError.'"
    return None



def test_check_length():
    seq4 = 'A' # Case 3 single amino acid
    seq5 = 'AAAAA' # Case 4 amino acid less than 11
    
    seqences = [seq4, 'AA', 'AAA', seq5, 'AAAAAAAAAA', 'AAAAAAAAAAA']

    for seq in seqences:
        try:
            check_inputs.check_length(seq)

        except Exception as exep:
            assert isinstance(exep, AssertionError), ("An unplanned error occured. Not an 'AssertionError.'"
                                                        " Error with test: " + str(seq))
    return None



def test_check_empty():
    seq1 = '                     ' # Case 2 empty string
    seq2 = 'ATG      LMCS        ' # Case 2 white space string
    seq3 = 'NaN'
    seq4 = 'NA'
    seq5 = ''
    seq6 = []

    seqences = [seq1, seq2, seq3, seq4, seq5, seq6]

    for seq in seqences:
        try:
            check_inputs.check_empty(seq)

        except Exception as exep:
            assert isinstance(exep, AssertionError), ("An unplanned error occured. Not an 'AssertionError.'"
                                                        " Error with test: " + str(seq))
    return None



def test_check_bad_chars():
    amino_acids = {'A':'Ala','G':'Gly','I':'Ile','L':'Leu','P':'Pro',
               'V':'Val','F':'Phe','W':'Trp','Y':'Tyr','D':'Asp',
               'E':'Glu','R':'Arg','H':'His','K':'Lys','S':'Ser',
               'T':'Thr','C':'Cys','M':'Met','N':'Asn','Q':'Gln',}
    
    seq7 = 'ATGILPQXMCTFWDPSCUAGINMWRTC' # Case 6: Ambigious AA's
    seq8 = 'ATGIL$PQWMCTFWDPSCUAGINMWRTC' # Case 7: Bad characters in AA string

    seqences = [seq7, seq8]

    for seq in seqences:
        try:
            check_inputs.check_bad_chars(seq, amino_acids)

        except Exception as exep:
            assert isinstance(exep, AssertionError), ("An unplanned error occured. Not an 'AssertionError.'"
                                                        " Error with test: " + str(seq))
    return None



def test_raise_error_bad_char():
    # try passing some invalid characters and see if it raises an error
    
    bad_characters = ['*', '.', '#', '$', 'X', '&', 'U', 'Z']

    try:
        check_inputs.raise_error_bad_char(bad_characters)

    except Exception as exep:
        assert isinstance(exep, AssertionError), ("An unplanned error occured. Not an 'AssertionError.'"
                                                    " Error with test: " + str(bad_characters))
    return None



def test_check_for_three_letter_code():
    amino_acids = {'A':'Ala','G':'Gly','I':'Ile','L':'Leu','P':'Pro',
           'V':'Val','F':'Phe','W':'Trp','Y':'Tyr','D':'Asp',
           'E':'Glu','R':'Arg','H':'His','K':'Lys','S':'Ser',
           'T':'Thr','C':'Cys','M':'Met','N':'Asn','Q':'Gln',}
    
    seq9 = 'AlaHisLysThrValPheMetLysProTrpAsnGlnIleGlyArgLysArgCysSer' # Case 8: Three letter AA codes
    seq10 = 'ALAHISLYSTHRVALPHEMETLYSPROTRPASNGLNILEGLYARGLYSARGCYSSER' # Case 9: Three letter AA codes all upper case
    seq11 = 'alahislysthrvalphemetlysprotrpasnglnileglyarglysargcysgly' # Case 10: Three letter AA codes all lower case

    seqences = [seq9, seq10, seq11]

    for seq in seqences:
        try:
            check_inputs.check_for_three_letter_code(seq, amino_acids)

        except Exception as exep:
            assert isinstance(exep, AssertionError), ("An unplanned error occured. Not an 'AssertionError.'"
                                                        " Error with test: " + str(seq))
    return None



def test_check_input():
    """Testing them all, because why not.
    """
    
    # 11 cases of different inputs cases.
    seq1 = 'ATGILPQNMCTFWDPSCVAGINMWRTC' # Case 1: Expected good input
    seq2 = '                     ' # Case 2 empty string
    seq3 = 'ATG      LMCS        ' # Case 3 white space string
    seq4 = 'A' # Case 4 single amino acid
    seq5 = 'AAAAA' # Case 5 amino acid less than 11
    seq6 = 4 # Case 6 number input
    seq7 = 'ATGILPQXMCTFWDPSCUAGINMWRTC' # Case 7: Ambigious AA's
    seq8 = 'ATGIL$PQWMCTFWDPSCUAGINMWRTC' # Case 8: Bad characters in AA string
    seq9 = 'AlaHisLysThrValPheMetLysProTrpAsnGlnIleGlyArgLysArgCysSer' # Case 9: Three letter AA codes
    seq10 = 'ALAHISLYSTHRVALPHEMETLYSPROTRPASNGLNILEGLYARGLYSARGCYSSER' # Case 10: Three letter AA codes all upper case
    seq11 = 'alahislysthrvalphemetlysprotrpasnglnileglyarglysargcysgly' # Case 11: Three letter AA codes all lower case

    seqences = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9, seq10, seq11]

    for seq in seqences:
        try:
            check_inputs.check_input(seq)

        except Exception as exep:
            assert isinstance(exep, AssertionError), ("An unplanned error occured. Not an 'AssertionError.'"
                                                        " Error with test: " + str(seq))
    return None







