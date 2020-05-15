import logging
from typing import Optional

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


class TrainView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):  #, generics.RetrieveAPIView):
    queryset = TrainSession.objects.all().order_by('-start_time')
    serializer_class = TrainSessionSerializer

    def run(self, request: Request, pk: Optional[int] = None, *args,
            **kwargs) -> Response:
        params = []
        if pk is None:
            # Train models for all parameters
            logging.debug('Running training sessions for all parameters')
            params = Parameters.objects.all()
        else:
            # Train model for only one parameter
            params = [Parameters.objects.get(pk=pk)]
        sessions = TrainSessionManager(store_class=TrainSession).run(params)
        return Response(TrainSessionSerializer(sessions, many=True).data)
