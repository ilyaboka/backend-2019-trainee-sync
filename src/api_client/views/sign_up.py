from typing import Dict

from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import SignUpPostRequest
from api_client.validation_serializers import SignUpPostResponse
from pitter import exceptions
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.models.user import User


class SignUpView(APIView):
    @classmethod
    @request_body_serializer(SignUpPostRequest)
    @response_dict_serializer(SignUpPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=SignUpPostRequest,
        responses=dict(
            [
                SignUpPostResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.ConflictError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Создание аккаунта',
        operation_description='Создание нового аккаунта',
    )
    def post(cls, request: Request) -> Dict[str, str]:
        """Создание аккаунта"""
        login: str = request.data['login']
        password: str = request.data['password']

        try:
            user = User.create_user(login=login, password=password)
        except IntegrityError as integrity_error:
            raise exceptions.ConflictError(f'Login {login} already in use') from integrity_error

        return dict(id=user.id, login=user.login,)
