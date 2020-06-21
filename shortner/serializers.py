# import random
# import string

from rest_framework import serializers

from shortner.models import URL


# def randomString(stringLength=8):
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(stringLength))


class CreateURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('original_url',)

    def create(self, validated_data):
        # import pdb;
        # pdb.set_trace()
        user = self.context['request'].user
        # validated_data['user'] = user#User(id=user)#.objects.get(id=user)
        # validated_data['short_url'] = randomString()

        # return URL.objects.create(**validated_data)
        return URL.objects.create(user=user, **validated_data)
        # return super(CreateURLSerializer, self).create(validated_data)


class OriginalURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ('original_url', 'short_url')
