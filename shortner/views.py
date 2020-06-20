from hashlib import md5

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from shortner.serializers import URLSerializer


# Create your views here.

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return JsonResponse(content)


class CreateShortURL(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = URLSerializer

    def post(self, request):
        # original_url = short_url = ""
        # import pdb;
        # pdb.set_trace()
        user_id = request.user.id
        original_url = request.POST.get('original_url', '')
        if original_url:
            validate = URLValidator()
            try:
                validate(original_url)
            except ValidationError:
                raise TypeError('URL not found.')

        short_url = md5(original_url.encode()).hexdigest()[:10]

        request_data = request.data.copy()

        serializer = self.serializer_class(data=request_data, context={'request': request})
        if serializer.is_valid():
            obj = serializer.save()
            obj.user = user_id
            obj.short_url = short_url
            obj.save()
            return JsonResponse(obj.data, status=200)
        return JsonResponse(serializer.errors, status=400)
