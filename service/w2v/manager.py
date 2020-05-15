from multiprocessing import Pool
import sys
from typing import Dict, List
import warnings
import uuid

import django
from sklearn.model_selection import ParameterGrid
import pytz

from train.models import TrainSessionModel

from .w2vmodel import W2VModel, run_model


class TrainSessionManager:
    def __init__(self):  #, pool=settings.POOL):
        self.experiment = uuid.uuid4()
        # self.pool = pool

    def _enumerate_search_space(self, request: Dict[str, List]) -> List:
        return list(ParameterGrid(request))

    def _close_db_connections(self):
        for name, info in django.db.connections.databases.items(
        ):  # Close the DB connections
            django.db.connection.close()

    def _create_training_session(self, params):
        session = TrainSessionModel.objects.create(
            experiment=self.experiment,
            status=TrainSessionModel.Created,
            param_start_alpha=params.get('start_alpha', None),
            param_end_alpha=params.get('end_alpha', None),
            param_epochs=params.get('epochs', None))
        return session

    def _create_model_training(self, params):
        """ Load pre-trained model and get it ready to run
        """
        experiment = uuid.uuid4()
        session = self._create_training_session(params)
        model = W2VModel(params=params, session=session)
        return model

    def _start_hyperparam_opt(self, request) -> List[W2VModel]:
        search_space = self._enumerate_search_space(request)
        models = []
        for params in search_space:
            model = self._create_model_training(params)
            models.append(model)
        return models, search_space

    def create(self, request: Dict) -> Dict:
        if (isinstance(request['start_alpha'], list)
                or isinstance(request['end_alpha'], list)
                or isinstance(request['epochs'], list)):
            models, search_space = self._start_hyperparam_opt(request)
            sessions = {
                model.session.id: params
                for model, params in zip(models, search_space)
            }
            result = dict(experiment=self.experiment, sessions=sessions)
        else:
            model = self._create_model_training(request)
            result = dict(experiment=self.experiment,
                          sessions={model.session.id: request})
        self._close_db_connections()
        pool = Pool(len(models))
        pool.map_async(run_model, models)
        return result