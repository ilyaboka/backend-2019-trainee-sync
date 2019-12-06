from http import HTTPStatus

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from pitter import exceptions
from pitter.decorators import access_token_required


class AccountView(APIView):
    @classmethod
    @access_token_required
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        responses=dict(
            [
                (HTTPStatus.NO_CONTENT.value, 'Success'),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.NotFoundError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Удаление аккаунта',
        operation_description='Удаление пользовательского аккаунта',
    )
    def delete(cls, request: Request) -> HttpResponse:
        """Удаление пользовательского аккаунта"""
        request.token_user.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT.value)
