from rest_framework import status
from rest_framework.response import Response


class CustomResponse():
    def __init__(self):
        pass

    @staticmethod
    def create_response(stat, resCode, message, data):
        return Response(
            {"status": stat, "code": resCode, "message": message, "data": data},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def create_error_response(resCode, message):
        return Response(
            {"status": 'false', "code": resCode, "message": message},
            status=status.HTTP_200_OK
        )
