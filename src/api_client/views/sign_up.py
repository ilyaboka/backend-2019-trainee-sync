from http import HTTPStatus

from django.db.utils import IntegrityError
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import SignUpPostRequest
from api_client.validation_serializers import SignUpPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.models.user import User


class SignUpView(APIView):
    @classmethod
    @request_post_serializer(SignUpPostRequest)
    @response_dict_serializer(SignUpPostResponse)
    @swagger_auto_schema(
        request_body=SignUpPostRequest,
        responses={
            HTTPStatus.OK.value: SignUpPostResponse,
            HTTPStatus.BAD_REQUEST.value: exceptions.ExceptionResponse,
            HTTPStatus.CONFLICT.value: exceptions.ExceptionResponse,
            HTTPStatus.UNPROCESSABLE_ENTITY.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Создание аккаунта',
        operation_description='Создание нового аккаунта',
    )
    def post(cls, request: Request) -> HttpResponse:
        """Создание аккаунта"""
        login: str = request.data['login']
        password: str = request.data['password']

        try:
            user = User.create_user(login=login, password=password)
        except IntegrityError as integrity_error:
            raise exceptions.ValidationError(
                'Login already in use', status_code=HTTPStatus.CONFLICT.value
            ) from integrity_error

        return dict(id=user.id, login=user.login,)
