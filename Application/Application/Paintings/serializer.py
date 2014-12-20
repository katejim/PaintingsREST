__author__ = 'kate'
from Application.Paintings.models import Pictures
from rest_framework import serializers


class AllPicturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pictures
        fields = ('id', 'name', 'link', 'type', 'price')
