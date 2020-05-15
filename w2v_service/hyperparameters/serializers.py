from rest_framework import serializers
from hyperparameters.models import Parameters


class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = '__all__'