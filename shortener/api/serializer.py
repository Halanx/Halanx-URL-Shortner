from rest_framework import serializers
from shortener.models import Url


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = [
            'pk',
            'url',
            'short',
            'updated',
            'created',
            'active',
            'count',
        ]
        read_only_fields = ['count', ]

