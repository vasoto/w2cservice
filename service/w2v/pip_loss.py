from typing import Union, List
import numpy as np


def pip_(x: Union[List, np.array]) -> np.float64:
    x = x / np.linalg.norm(x)
    return x.dot(x.T)


def pip_distance(x: Union[List, np.array],
                 y: Union[List, np.array]) -> np.float64:
    return np.linalg.norm((pip_(x) - pip_(y)))


# may need to adjust the below function if it is not working correctly for your w2v model
def make_fingerprint_matrix(w2v_model, concepts):
    vectors = [
        w2v_model.wv[c]
        if c in w2v_model.wv else np.zeros(w2v_model.vector_size)
        for c in concepts
    ]
    fingerprint_matrix = np.array([v for v in vectors])
    return fingerprint_matrix


def calculate_pip_distance(reference_words_list, reference_word_model_matrix,
                           w2v_model_to_compare):
    # for reference_words_list use the words from ref_vocab.json
    words_matrix_1 = reference_word_model_matrix  # load using pickle python module from file ref_vocab_matrix.pkl
    words_matrix_2 = make_fingerprint_matrix(w2v_model_to_compare,
                                             reference_words_list)
    return pip_distance(words_matrix_1, words_matrix_2)