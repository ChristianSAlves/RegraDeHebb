from rest_framework import serializers
from .models import HebbModel

class MatrixSerializer(serializers.Serializer):
    matrix = serializers.ListField(
        child=serializers.IntegerField(min_value=-1, max_value=1),
        max_length=100
    )

class HebbModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HebbModel
        fields = ['id', 'weights', 'bias']
