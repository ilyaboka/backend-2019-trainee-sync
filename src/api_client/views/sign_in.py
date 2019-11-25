from datetime import datetime
from http import HTTPStatus

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from jwt import encode
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import SignInPostRequest
from api_client.validation_serializers import SignInPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import User
from pitter.settings import JSON_WEB_TOKEN_LIFETIME
from pitter.settings import JSON_WEB_TOKEN_PRIVATE_KEY


class SignInView(APIView):
    @classmethod
    @request_post_serializer(SignInPostRequest)
    @response_dict_serializer(SignInPostResponse)
    @swagger_auto_schema(
        request_body=SignInPostRequest,
        responses={
            HTTPStatus.OK.value: SignInPostResponse,
            HTTPStatus.BAD_REQUEST.value: exceptions.ExceptionResponse,
            HTTPStatus.UNPROCESSABLE_ENTITY.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Вход в систему',
        operation_description='Вход в систему, получение JWT',
    )
    def post(cls, request: Request) -> HttpResponse:
        """Вход в систему, получение JWT"""
        try:
            user: User = User.objects.get(login=request.data['login'])
            if user.has_password(request.data['password']):
                return dict(
                    token=encode(
                        dict(exp=datetime.utcnow() + JSON_WEB_TOKEN_LIFETIME, id=user.id,),
                        JSON_WEB_TOKEN_PRIVATE_KEY,
                        algorithm='RS256',
                    ).decode('ascii'),
                )
            raise exceptions.ValidationError('Invalid credentials', status_code=HTTPStatus.BAD_REQUEST.value)
        except User.DoesNotExist as does_not_exist:
            raise exceptions.ValidationError(
                'Invalid credentials', status_code=HTTPStatus.BAD_REQUEST.value
            ) from does_not_exist
        except UnicodeError as unicode_error:
            raise exceptions.PitterException(
                'Something went wrong', 'Server Error', status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value
            ) from unicode_error
