import hashlib

from django.core.validators import URLValidator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from shortner.models import URL
from shortner.serializers import CreateURLSerializer, OriginalURLSerializer
from shortner.utils import CustomResponse


# Create your views here.


class CreateShortURL(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateURLSerializer

    def post(self, request):
        original_url = request.POST.get('original_url', '') if request.POST.get('original_url') else request.data.get(
            'original_url', '')

        if not original_url:
            return CustomResponse.create_error_response(status.HTTP_200_OK, 'original_url field is required.')

        validate = URLValidator()
        try:
            validate(original_url)
        except:
            return CustomResponse.create_error_response(status.HTTP_200_OK, 'Invalid given url.')

        result = URL.objects.filter(original_url=original_url)
        if result:
            return CustomResponse.create_error_response(status.HTTP_200_OK, 'This url is already shortened.')

        short_url = hashlib.md5(original_url.encode()).hexdigest()[:10]

        request_data = request.data.copy()
        request_data['user'] = request.user.id
        request_data['short_url'] = short_url

        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.create_response(True, status.HTTP_201_CREATED, 'Success', serializer.data)

        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class GetOriginalURL(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OriginalURLSerializer

    def post(self, request):
        short_url = request.POST.get('short_url', '') if request.POST.get('short_url') else request.data.get(
            'short_url', '')
        if short_url:
            try:
                result = URL.objects.get(short_url=short_url)
                serializer = self.serializer_class(result, context={'request': request}, many=False)
                return CustomResponse.create_response(True, status.HTTP_200_OK, 'Success', serializer.data)
            except:
                return CustomResponse.create_error_response(status.HTTP_200_OK, 'Url not found')

        return CustomResponse.create_error_response(status.HTTP_200_OK, 'short_url field is required.')
