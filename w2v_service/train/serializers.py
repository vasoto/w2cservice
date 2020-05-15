from rest_framework import serializers
from train.models import TrainSession


class TrainSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainSession
        fields = '__all__'