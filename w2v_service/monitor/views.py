from collections import defaultdict
import logging
from typing import Optional

from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.request import Request

from train.models import TrainSession
from train.serializers import TrainSessionSerializer
from hyperparameters.models import Parameters
from hyperparameters.serializers import ParametersSerializer
from w2v.manager import TrainSessionManager

logger = logging.getLogger(__name__)


def aggregate_by_params(sessions):
    data = defaultdict(list)
    for session in sessions:
        if session.result is None:
            continue
        data[session.parameters].append(
            dict(pip_loss=session.result, filename=session.file_name))
    return data


class MonitorView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = TrainSession.objects.all().order_by('-start_time')
    serializer_class = TrainSessionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TrainSession.objects.all()
        start_alpha = self.request.query_params.get('start_alpha', None)
        end_alpha = self.request.query_params.get('end_alpha', None)
        epochs = self.request.query_params.get('epochs', None)
        print("QP:", self.request.query_params)
        if epochs is not None:
            queryset = queryset.filter(parameters__epochs=int(epochs))
        if start_alpha is not None:
            queryset = queryset.filter(
                parameters__start_alpha=float(start_alpha))
            print(queryset)
        if end_alpha is not None:
            queryset = queryset.filter(parameters__end_alpha=float(end_alpha))
        return queryset

    def list(self, request, *args, **kwargs):
        sessions = self.get_queryset()

        print(sessions)

        # sessions = TrainSession.objects.filter(
        #     parameters__in=parameters,
        #     status=TrainSession.Finished).select_related().order_by(
        #         'parameters')
        result = [
            dict(start_alpha=parameters.start_alpha,
                 end_alpha=parameters.end_alpha,
                 epochs=parameters.epochs,
                 results=results)
            for parameters, results in aggregate_by_params(sessions).items()
        ]
        return Response(result)
