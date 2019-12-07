from http import HTTPStatus
from typing import Dict

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import EmailNotificationsEnabledGetResponse
from api_client.validation_serializers import EmailNotificationsEnabledPostRequest
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import User


class EmailNotificationsEnabledView(APIView):
    @classmethod
    @access_token_required
    @response_dict_serializer(EmailNotificationsEnabledGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        responses=dict(
            [
                EmailNotificationsEnabledGetResponse.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Получение статуса оповещений на email',
        operation_description='Получение статуса оповещений на email',
    )
    def get(cls, request: Request) -> Dict[str, bool]:
        """Получение статуса оповещений на email"""
        response: Dict[str, bool] = dict(enabled=request.token_user.email_notifications_enabled)
        return response

    @classmethod
    @access_token_required
    @request_body_serializer(EmailNotificationsEnabledPostRequest)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=EmailNotificationsEnabledPostRequest,
        responses=dict(
            [
                (HTTPStatus.OK.value, 'Success'),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.UnprocessableEntityError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Установка статуса оповещений на email',
        operation_description='Установка статуса оповещений на email',
    )
    def post(cls, request: Request) -> HttpResponse:
        """Установка статуса оповещений на email"""
        user: User = request.token_user
        enabled: bool = request.data['enabled']
        if enabled and not user.email_address:
            raise exceptions.UnprocessableEntityError("Can't enable notifications: set email address first")
        user.email_notifications_enabled = request.data['enabled']
        user.save()
        response: HttpResponse = HttpResponse()
        return response
