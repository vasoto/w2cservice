from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.request import Request

from hyperparameters.models import Parameters
from hyperparameters.serializers import ParametersSerializer
from w2v.utils import enumerate_parameters


class ParametersView(mixins.ListModelMixin, mixins.CreateModelMixin,
                     viewsets.GenericViewSet):  #, generics.RetrieveAPIView):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer

    # def list(self, request, *args, **kwargs):
    #     print("LIST", request.data, args, kwargs)
    #     return Response([])

    def create(self, request: Request, *args, **kwargs) -> Response:
        params = []

        if any([isinstance(param, list) for param in request.data.values()]):
            params = enumerate_parameters(request.data)
        else:
            params = [request.data]  # single set of parameters
        # Create hyperparametric space
        instances = []
        for param_set in params:
            try:
                instance = Parameters.objects.create(
                    start_alpha=param_set.get('start_alpha', None),
                    end_alpha=param_set.get('end_alpha', None),
                    epochs=param_set.get('epochs', None))
            except IntegrityError as err:
                instances.append(
                    dict(
                        error=
                        f'The set of parameters {param_set} is already entered.'
                    ))
            else:
                instances.append(ParametersSerializer(instance).data)
        # result = ParametersSerializer(instances, many=True).data
        return Response(instances)

    def list(self, request: Request, *args, **kwargs) -> Response:
        param_sets = Parameters.objects.all()
        serializer = ParametersSerializer(param_sets, many=True)
        return Response(serializer.data)
