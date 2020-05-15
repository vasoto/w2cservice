from rest_framework import serializers
from train.models import TrainSessionModel


class TrainSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainSessionModel
        fields = '__all__'

    # def create(self, validated_data):
    #     address_data = validated_data.pop('adresse')
    #     address = Adresse.objects.create(**address_data)
    #     organism = Organisme.objects.create(address=address, **validated_data)
    #     return organism
