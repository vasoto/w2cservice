import sys
from typing import Dict, List

from gensim.models import Word2Vec

import django
django.setup()  # Must call setup
from django.utils import timezone

from train.models import TrainSessionModel

from .utils import load_ref_data, load_vocabulary
from .pip_loss import calculate_pip_distance

REF_DATA, REF_MATRIX = load_ref_data()
VOCABULARY = load_vocabulary()


class W2VModel:
    def __init__(self,
                 params,
                 session,
                 ref_data=REF_DATA,
                 ref_matrix=REF_MATRIX,
                 vocabulary=VOCABULARY):
        self.params = params
        self.model = None
        self.callbacks = []
        self.session = session
        self.ref_data = ref_data
        self.ref_matrix = ref_matrix
        self.vocabulary = vocabulary

    def _get_error_info(self):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return exc_type, fname, exc_tb.tb_lineno

    def load(self):
        # TODO: get path from django settings
        try:
            self.model = Word2Vec.load(
                "../third/materials-word-embeddings/bin/word2vec_embeddings-SNAPSHOT.model"
            )
            self.model.build_vocab(self.vocabulary, update=True)
        except Exception as err:
            print(err)
            self.set_status(TrainSessionModel.Error,
                            result=str(err),
                            is_last=True)
            return False
        print(f'Model loaded {len(self.vocabulary)}')
        return True

    def set_status(self, status, result=None, is_last=False, is_start=False):
        self.session.status = status
        if result:
            self.session.result = result
        if is_start and is_last:
            warnings.warn('Setting status with both is_start and is_end')
        if is_start:
            self.session.start_time = timezone.now()
        if is_last:
            self.session.end_time = timezone.now()
        self.session.save()

    def monitor(self, event_type: str, payload: str) -> None:
        pass

    def eval_model(self) -> Dict:
        return f"pip: {calculate_pip_distance(self.ref_data, self.ref_matrix, self.model)}"

    def train(self):
        result = None
        status = TrainSessionModel.Running
        print("Train started")
        try:
            self.set_status(status=TrainSessionModel.Running, is_start=True)
            print(f"Going to train with params {self.params}")
            self.model.train(**self.params,
                             sentences=self.vocabulary,
                             total_examples=len(self.vocabulary))
            # callbacks=self.callbacks)
            result = self.eval_model()
            status = TrainSessionModel.Finished
        except Exception as err:
            result = str(err)
            status = TrainSessionModel.Error
            print(f"Error: {result}")
        finally:
            self.set_status(status=status, result=result, is_last=True)
        print("Train ended")


def run_model(model: W2VModel) -> None:
    from django.db import connections
    from django.db.utils import DEFAULT_DB_ALIAS
    try:
        connections.close_all()
        if model.load():
            model.train()
    except Exception as err:
        print(err)