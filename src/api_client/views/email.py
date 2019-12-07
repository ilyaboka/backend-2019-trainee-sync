from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import EmailPostRequest
from api_client.validation_serializers import EmailPostResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import User


class EmailView(APIView):
    @classmethod
    @access_token_required
    @request_body_serializer(EmailPostRequest)
    @response_dict_serializer(EmailPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=EmailPostRequest,
        responses=dict(
            [
                EmailPostResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Установка email',
        operation_description='Установка email адреса пользователя',
    )
    def post(cls, request: Request) -> Dict[str, str]:
        """Установка email адреса пользователя"""
        user: User = request.token_user
        email: str = request.data['email']
        user.email_address = email
        user.save()
        response: Dict[str, str] = dict(email=email)
        return response
