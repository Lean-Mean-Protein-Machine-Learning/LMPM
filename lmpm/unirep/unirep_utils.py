import os

import numpy as np


"""Dictionary for converting amino acids to their integer key value"""
aa_to_int = {
    "-": 0,
    "M": 1,
    "R": 2,
    "H": 3,
    "K": 4,
    "D": 5,
    "E": 6,
    "S": 7,
    "T": 8,
    "N": 9,
    "Q": 10,
    "C": 11,
    "U": 12,
    "G": 13,
    "P": 14,
    "A": 15,
    "V": 16,
    "I": 17,
    "F": 18,
    "Y": 19,
    "W": 20,
    "L": 21,
    "O": 22,  # Pyrrolysine
    "X": 23,  # Unknown
    "Z": 23,  # Glutamic acid or GLutamine
    "B": 23,  # Asparagine or aspartic acid
    "J": 23,  # Leucine or isoleucine
    "start": 24,
    "stop": 25,
}


def my_seq_to_ints(seq):
    return [24] + [aa_to_int[a] for a in list(seq)] + [25]


def my_get_embeddings(sequence, embeddings):
    sequence = my_seq_to_ints(sequence)[:-1]
    x = np.vstack([embeddings[i] for i in sequence])
    return x


"""Neural network utility functions, including activations and normalization"""


def sigmoid(x, version="tanh"):
    sigmoids = {
        "tanh": lambda x: 0.5 * np.tanh(x) + 0.5,
        "exp": lambda x: safe_sigmoid_exp(x),
    }
    return sigmoids[version](x)


def tanh(x):
    return np.tanh(x)


def safe_sigmoid_exp(x, clip_value=-88):
    x = np.clip(x, a_min=-88, a_max=None)
    return 1 / (1 + np.exp(-x))


def l2_normalize(arr, axis, epsilon=1e-12):
    sq_arr = np.power(arr, 2)
    square_sum = np.sum(sq_arr, axis=axis, keepdims=True)
    max_weights = np.maximum(square_sum, epsilon)
    return np.divide(arr, np.sqrt(max_weights))


"""Define function for loading weights from directory"""


def load_weights():
    params = {}
    dir_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "weight_files/"
    )
    for file in os.listdir(dir_path):
        if file[-4:] == ".npy":
            if file.split("_weights")[0] == "embedding":
                embedding_weights = np.load(os.path.join(dir_path, file))
            else:
                params[file.split("_weights_")[-1].split(".npy")[0]] = np.load(
                    os.path.join(dir_path, file)
                )
    return embedding_weights, params


"""Load all weights"""
embedding_weights, params = load_weights()

""" pre-normalize weights, because that's what took so long to compute"""
wx = l2_normalize(params["wx"], axis=0) * params["gx"]
wh = l2_normalize(params["wh"], axis=0) * params["gh"]
wmx = l2_normalize(params["wmx"], axis=0) * params["gmx"]
wmh = l2_normalize(params["wmh"], axis=0) * params["gmh"]


def mLSTMCell(carry, x_t):
    h_t, c_t = carry

    # Shape annotation
    # (:, 10) @ (10, n_outputs) * (:, n_outputs) @ (n_outputs, n_outputs) => (:, n_outputs)  # noqa: E501
    m = np.matmul(x_t, wmx) * np.matmul(h_t, wmh)

    # (:, 10) @ (10, n_outputs * 4) * (:, n_outputs) @ (n_outputs, n_outputs * 4) + (n_outputs * 4, ) => (:, n_outputs * 4)  # noqa: E501
    z = np.matmul(x_t, wx) + np.matmul(m, wh) + params["b"]

    # Splitting along axis 1, four-ways, gets us (:, n_outputs) as the shape  # noqa: E501
    # for each of i, f, o and u
    i, f, o, u = np.split(z, 4, axis=-1)  # input, forget, output, update

    # Elementwise transforms here.
    # Shapes are are (:, n_outputs) for each of the four.
    i = sigmoid(i, version="exp")
    f = sigmoid(f, version="exp")
    o = sigmoid(o, version="exp")
    u = tanh(u)

    # (:, n_outputs) * (:, n_outputs) + (:, n_outputs) * (:, n_outputs) => (:, n_outputs)  # noqa: E501
    c_t = f * c_t + i * u

    # (:, n_outputs) * (:, n_outputs) => (:, n_outputs)
    h_t = o * tanh(c_t)

    # h, c each have shape (:, n_outputs)
    return (h_t, c_t), h_t


def scan(f, init, xs, length=None):
    if xs is None:
        xs = [None] * length
    carry = init
    ys = []

    for x in xs:
        carry, y = f(carry, x)
        ys.append(y)

    return carry, np.stack(ys)


def get_UniReps(seqs):

    h_avg_list = []

    if isinstance(seqs, str):
        seqs = [seqs]

    for seq in seqs:
        x = my_get_embeddings(seq, embedding_weights)
        h_t = np.zeros(params["wmh"].shape[0])
        c_t = np.zeros(params["wmh"].shape[0])

        outputs = scan(mLSTMCell, init=(h_t, c_t), xs=x)[1]

        h_avg = outputs.mean(axis=0)

        h_avg_list.append(h_avg)

    return np.stack(h_avg_list)
