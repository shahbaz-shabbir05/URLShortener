from rest_framework import serializers

from shortner.models import URL


class CreateURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('original_url', 'short_url')

    def create(self, validated_data):
        user = self.context['request'].user

        return URL.objects.create(user=user, **validated_data)


class OriginalURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('original_url', 'short_url')
