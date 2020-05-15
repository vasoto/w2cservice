from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from train.models import TrainSessionModel
from train.serializers import TrainSessionSerializer
from w2v.manager import TrainSessionManager


class TrainSessionView(
        viewsets.ModelViewSet
):  # generics.ListCreateAPIView, generics.RetrieveAPIView):
    queryset = TrainSessionModel.objects.all().order_by('-start_time')
    serializer_class = TrainSessionSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        manager = TrainSessionManager()
        result = manager.create(request.data)
        return Response({'result': result})


class ExperimentsView(
        viewsets.ModelViewSet
):  # generics.ListCreateAPIView, generics.RetrieveAPIView):
    queryset = TrainSessionModel.objects.all().order_by('-start_time')
    serializer_class = TrainSessionSerializer

    # @action(detail=True)
    # def experiment(self, request, *args, **kwargs):
    #     # snippet = self.get_object()
    #     return Response({})

    def retrieve(self, request, pk, *args, **kwargs):
        print("RETRIEVE", args, kwargs)
        sessions = TrainSessionModel.objects.filter(experiment=pk)
        print(sessions)
        serializer = TrainSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = TrainSessionModel.objects.values('experiment').distinct()
        experiments = queryset  #set([session.experiment for session in queryset])
        # serializer = TrainSessionSerializer(queryset, many=True)
        # print(serializer)
        return Response(experiments)
