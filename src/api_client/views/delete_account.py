from django.http import HttpResponse
from django.db.models.query import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import DeleteAccountPostRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer

from pitter.models.user import User


class DeleteAccountView(APIView):
    @classmethod
    @request_post_serializer(DeleteAccountPostRequest)
    @swagger_auto_schema(
        tags=["Pitter: mobile"],
        request_body=DeleteAccountPostRequest,
        responses={200: 'Success', 404: exceptions.ExceptionResponse, 500: exceptions.ExceptionResponse,},
        operation_summary='Удаление аккаунта',
        operation_description='Удаление пользовательского аккаунта',
    )
    def post(cls, request: Request) -> HttpResponse:
        """
        Преобразование речи в текст с использованием Google Speech-To-Text
        :param request:
        :return:
        """
        user: QuerySet = User.objects.filter(login=request.data['login'])
        if user:
            user.delete()
            return HttpResponse(status=200)
        raise exceptions.ValidationError('Login not found', status_code=404)
