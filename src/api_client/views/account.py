from http import HTTPStatus

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import AccountDeleteRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer

from pitter.models.user import User


class AccountView(APIView):
    @classmethod
    @request_post_serializer(AccountDeleteRequest)
    @swagger_auto_schema(
        request_body=AccountDeleteRequest,
        responses={
            HTTPStatus.NO_CONTENT.value: 'Success',
            HTTPStatus.NOT_FOUND.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление аккаунта',
        operation_description='Удаление пользовательского аккаунта',
    )
    def delete(cls, request: Request) -> HttpResponse:
        """Удаление пользовательского аккаунта"""
        try:
            User.objects.get(id=request.data['id']).delete()
            return HttpResponse(status=HTTPStatus.NO_CONTENT.value)
        except User.DoesNotExist:
            raise exceptions.ValidationError('User not found', status_code=HTTPStatus.NOT_FOUND.value)
