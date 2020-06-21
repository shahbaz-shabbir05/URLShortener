from rest_framework import serializers

from shortner.models import URL


class CreateURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('user', 'original_url', 'short_url')

    def create(self, validated_data):
        return URL.objects.create(**validated_data)


class OriginalURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('user', 'original_url',)
