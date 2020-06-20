from rest_framework import serializers

from shortner.models import URL


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('original_url',)  # 'short_url')

    def create(self, validated_data):
        # import pdb;
        # pdb.set_trace()
        user = self.context['request'].user
        # if 'user' not in validated_data:
        #     validated_data['user'] = 0#self.context['request'].user

        return URL.objects.create(user=user, **validated_data)

        # return super(URLSerializer, self).create(validated_data)
