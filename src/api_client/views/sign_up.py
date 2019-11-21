from django.http import HttpResponse
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import SignUpPostRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer

from pitter.models.user import User


class SignUpView(APIView):
    @classmethod
    @request_post_serializer(SignUpPostRequest)
    @swagger_auto_schema(
        tags=["Pitter: mobile"],
        request_body=SignUpPostRequest,
        responses={200: 'Success', 409: exceptions.ExceptionResponse, 500: exceptions.ExceptionResponse,},
        operation_summary='Создание аккаунта',
        operation_description='Создание нового аккаунта',
    )
    def post(cls, request: Request) -> HttpResponse:
        """
        Преобразование речи в текст с использованием Google Speech-To-Text
        :param request:
        :return:
        """
        try:
            User.create_user(login=request.data['login'], password=request.data['password'])
            return HttpResponse(200)
        except IntegrityError as integrity_error:
            raise exceptions.ValidationError('Login already in use', status_code=409) from integrity_error
