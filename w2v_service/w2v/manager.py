import logging
from multiprocessing import Pool
import sys
from typing import Dict, List
import warnings
import uuid

import django
from sklearn.model_selection import ParameterGrid

from .w2vmodel import W2VModel, run_model

logger = logging.getLogger(__name__)


class TrainSessionManager:
    """ Creates training sessions and train model for each parameter combination
    """
    def __init__(self, store_class):
        self.store_class = store_class

    def _get_params_fom_obj(self, parameters_obj) -> Dict:
        return {
            k: v
            for k, v in parameters_obj.__dict__.items()
            if k in ('start_alpha', 'end_alpha', 'epochs')
        }

    def create_models(self, parameters: List[Dict]) -> List:
        models = []
        for param_obj in parameters:
            try:
                session = self.store_class.objects.create(parameters=param_obj)
                params = self._get_params_fom_obj(param_obj)
                print(params)
                model = W2VModel(params, session)
            except Exception as err:
                logger.error("Error while trying to create train session: %s",
                             err)
            else:
                models.append(model)
        return models

    def run(self, parameters: List[Dict]) -> Dict:
        """ Create models and corresponding sessions and train models
        """
        models = self.create_models(parameters)
        if models:
            # Create process pool
            pool = Pool(len(models))
            pool.map_async(run_model, models)

        return [model.session for model in models]