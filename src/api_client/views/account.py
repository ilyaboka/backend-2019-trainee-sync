from http import HTTPStatus

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.models.user import User


class AccountView(APIView):
    @classmethod
    @access_token_required
    @swagger_auto_schema(
        responses={
            HTTPStatus.NO_CONTENT.value: 'Success',
            HTTPStatus.UNAUTHORIZED.value: exceptions.ExceptionResponse,
            HTTPStatus.NOT_FOUND.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление аккаунта',
        operation_description='Удаление пользовательского аккаунта',
    )
    def delete(cls, user_id: str, request: Request) -> HttpResponse:
        """Удаление пользовательского аккаунта"""
        try:
            user: User = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.ValidationError('User not found', status_code=HTTPStatus.NOT_FOUND.value)

        user.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT.value)
