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
        read_only_fields = ['count', 'short']

    @staticmethod
    def validate_url(value):
        qs = Url.objects.filter(url__iexact=value)
        if qs.exists():
            for e in qs:
                raise serializers.ValidationError(
                    "Shortened URL already exists. " + "url:" + e.url + "  shortcode:" + e.short)

        return value
