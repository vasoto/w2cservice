
import json
import os
import pickle
from typing import List, Dict

from sklearn.model_selection import ParameterGrid


def enumerate_parameters(params: Dict[str, List]) -> List[Dict]:
    return list(ParameterGrid(params))

def load_ref_data(data_dir:str):
    """ Load reference data for testing
    """
    with open(os.path.join(data_dir, 'ref_vocab.json'), 'r') as ref_data_file:
        ref_data = json.load(ref_data_file)

    with open(os.path.join(data_dir, 'ref_vocab_matrix.pkl'), 'rb') as ref_matrix_file:
        ref_matrix = pickle.load(ref_matrix_file)
    return ref_data, ref_matrix

def load_vocabulary(dataset_file:str):
    """ Load vocabulary training data
    """
    with open(dataset_file, 'rb') as datafile:
        data = pickle.load(datafile)
    return data