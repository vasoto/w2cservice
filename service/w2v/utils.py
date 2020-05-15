
import json
import os
import pickle

from django.conf import settings


def load_ref_data(data_dir:str=settings.DATA_DIR):
    """ Load reference data for testing
    """
    with open(os.path.join(data_dir, 'ref_vocab.json'), 'r') as ref_data_file:
        ref_data = json.load(ref_data_file)

    with open(os.path.join(data_dir, 'ref_vocab_matrix.pkl'), 'rb') as ref_matrix_file:
        ref_matrix = pickle.load(ref_matrix_file)
    return ref_data, ref_matrix

def load_vocabulary(dataset_file:str = settings.DATASET_FILE):
    """ Load vocabulary training data
    """
    with open(dataset_file, 'rb') as datafile:
        data = pickle.load(datafile)
    return data