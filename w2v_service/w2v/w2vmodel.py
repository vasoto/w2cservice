import datetime
import logging
import os
import sys
from typing import Dict, List

from gensim.models import Word2Vec

import django
django.setup()  # Must call setup
from django.conf import settings

from train.models import TrainSession

from .utils import load_ref_data, load_vocabulary
from .pip_loss import calculate_pip_distance

REF_DATA, REF_MATRIX = load_ref_data(settings.DATA_DIR)
VOCABULARY = load_vocabulary(settings.DATASET_FILE)

logger = logging.getLogger(__name__)


class W2VModel:
    def __init__(self,
                 params,
                 session,
                 models_output_dir=settings.MODELS_DIR,
                 base_model=settings.BASE_MODEL_FILE,
                 ref_data=REF_DATA,
                 ref_matrix=REF_MATRIX,
                 vocabulary=VOCABULARY):
        self.params = params
        self.model = None
        self.callbacks = []
        self.models_output_dir = models_output_dir
        self.base_model = base_model
        self.session = session
        self.ref_data = ref_data
        self.ref_matrix = ref_matrix
        self.vocabulary = vocabulary

    def load(self):
        try:
            self.model = Word2Vec.load(self.base_model)
            self.model.build_vocab(self.vocabulary, update=True)
        except Exception as err:
            self.session.set_status(TrainSession.Error,
                                    result=str(err),
                                    is_last=True)
            return False
        logger.debug(f'Model loaded')
        self.session.set_status(status=TrainSession.Loaded)
        return True

    def monitor(self, event_type: str, payload: str) -> None:
        pass

    def eval_model(self) -> Dict:
        return calculate_pip_distance(self.ref_data, self.ref_matrix,
                                      self.model)

    def train(self):
        result = None
        status = TrainSession.Running
        try:
            self.session.set_status(status=TrainSession.Running, is_start=True)
            logger.info("Going to train model with parameters %s", self.params)
            self.model.train(**self.params,
                             sentences=self.vocabulary,
                             total_examples=len(self.vocabulary))
            # callbacks=self.callbacks)
            result = self.eval_model()
            file_name = os.path.join(
                self.models_output_dir,
                'w2v_start_alpha-{start_alpha}_end_alpha-{end_alpha}_epochs-{epochs}-{dt:%Y%m%d%H%M%S}.model'
                .format(dt=datetime.datetime.now(), **self.params))
            self.model.save(file_name)
            self.session.file_name = file_name
            self.session.set_status(status=TrainSession.Finished,
                                    result=result,
                                    is_last=True)
        except Exception as err:
            self.session.set_status(status=TrainSession.Error,
                                    error=str(err),
                                    is_last=True)
            logger.error("Error while training model: %s", err)
        logger.info("Training model with parameters %s ended", self.params)


def run_model(model: W2VModel) -> None:
    from django.db import connections
    # from django.db.utils import DEFAULT_DB_ALIAS
    try:
        connections.close_all()
        if model.load():
            model.train()
    except Exception as err:
        print(err)