import hashlib

from django.core.validators import URLValidator
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from shortner.models import URL
from shortner.serializers import CreateURLSerializer, OriginalURLSerializer
from shortner.utils import CustomResponse


# Create your views here.

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)


class CreateShortURL(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateURLSerializer

    def post(self, request):
        # import pdb;
        # pdb.set_trace()
        user = request.user
        original_url = request.POST.get('original_url', '')
        if original_url:
            validate = URLValidator()
            try:
                validate(original_url)
            except:
                return CustomResponse.create_error_response(status.HTTP_200_OK, 'Invalid URL')

            result = URL.objects.filter(original_url=original_url)
            if result:
                return CustomResponse.create_error_response(status.HTTP_200_OK, 'URL already exist.')

            short_url = hashlib.md5(original_url.encode()).hexdigest()[:10]
        else:
            short_url = ''
        # request_data = request.data.copy()

        # serializer = self.serializer_class(data=request_data, context={'request': request})
        # if serializer.is_valid():
        #     obj = serializer.save()
        #     obj.user = user
        #     obj.short_url = short_url
        #     obj.save()
        # return JsonResponse(serializer.errors, status=400)
        url_obj = URL(original_url=original_url, short_url=short_url, user=user)
        url_obj.save()
        data = {"original_url": original_url, "short_url": short_url}
        return CustomResponse.create_response(True, status.HTTP_200_OK, 'Success', data)


class GetOriginalURL(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OriginalURLSerializer

    def post(self, request):
        short_url = request.POST.get('short_url', '')
        if short_url:
            try:
                result = URL.objects.get(short_url=short_url)
                serializer = self.serializer_class(result, context={'request': request}, many=False)
                return CustomResponse.create_response(True, status.HTTP_200_OK, 'Success', serializer.data)
            except:
                return CustomResponse.create_error_response(status.HTTP_200_OK, 'Invalid URL')

        return CustomResponse.create_error_response(status.HTTP_200_OK, 'No URL found.')
