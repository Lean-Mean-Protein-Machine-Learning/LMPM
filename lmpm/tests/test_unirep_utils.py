"""
Write tests for the predict.py functions.
"""

import lmpm.unirep.unirep_utils as unirep_utils


def test_my_seq_to_ints():
    seqs = ['ALIENSRCMING','invalidAAstring']
    for seq in seqs:
        try:
            unirep_utils.my_seq_to_ints(seq)
        except:
            assert False, "Passing invalid sequences did not raise an error"


# def test_my_get_embeddings():
#     unirep_utils.my_get_embeddings(sequence, embeddings)



def test_sigmoid():
    xs = [42, 'alien_number']
    for x in xs:
        try:
            unirep_utils.sigmoid(x, version="tanh")
        except:
            assert False, "Passing invalid values in sigmoid did not raise an error"


def test_tanh():
    xs = [42, 'alien_number']
    for x in xs:
        try:
            unirep_utils.tanh(x)
        except:
            assert False, "Passing invalid values in tanh did not raise an error"



def test_safe_sigmoid_exp():
    xs = [42, 'alien_number']
    for x in xs:
        try:
            unirep_utils.safe_sigmoid_exp(x, clip_value=-88)
        except:
            assert False, "Passing invalid values in safe_sigmoid_exp did not raise an error"


# def test_l2_normalize():
#     unirep_utils.l2_normalize(arr, axis, epsilon=1e-12)


# def test_mLSTMCell():
#     unirep_utils.mLSTMCell(carry,x_t)



def test_scan():
    try:
        unirep_utils.scan(unirep_utils.mLSTMCell,init=(34,24), xs = None, length=8)
    except Exception as e:
        assert isinstance(e, ValueError), "Passing incorrect values to scan did not raise a ValueError"


def test_get_UniReps():
    seqs = ['ALIENSRCMING','invalidaastring']
    for seq in seqs:
        try:
            unirep_utils.get_UniReps(seq)
        except:
            assert False, "Passing invalid sequences did not raise an error"
