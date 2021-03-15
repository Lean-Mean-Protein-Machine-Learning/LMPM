"""
Write tests for the predict.py functions.
"""

import lmpm.unirep.unirep_utils as unirep_utils


def test_my_seq_to_ints():
    seq = 'ALIENSRCMING'
    try:
        unirep_utils.my_seq_to_ints(seq)
    except:
        assert False, "Aliens are coming"


# def test_my_get_embeddings():
#     unirep_utils.my_get_embeddings(sequence, embeddings)



def test_sigmoid():
    x = 42
    try:
        unirep_utils.sigmoid(x, version="tanh")
    except:
        assert False, "Aliens are coming!"


def test_tanh():
    x = 42
    try:
        unirep_utils.tanh(x)
    except:
        assert False, "Aliens are coming!!"


def test_safe_sigmoid_exp():
    x = 42
    try:
        unirep_utils.safe_sigmoid_exp(x, clip_value=-88)
    except:
        assert False, "Aliens are coming!!!"


# def test_l2_normalize():
#     unirep_utils.l2_normalize(arr, axis, epsilon=1e-12)



def test_load_weights():
    try:
        unirep_utils.load_weights()
    except:
        assert False, "Aliens are coming!!!!"



# def test_mLSTMCell():
#     unirep_utils.mLSTMCell(carry,x_t)



# def test_scan():
#     unirep_utils.scan(f, init, xs, length=None)



def test_get_UniReps():
    seq = 'ALIENSRCMING'

    try:
        unirep_utils.get_UniReps(seq)
    except:
        assert False, "Aliens are coming!!!!!"






