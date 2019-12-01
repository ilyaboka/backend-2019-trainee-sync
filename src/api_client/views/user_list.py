from http import HTTPStatus
from typing import List

from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import UserListGetResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import response_list_serializer
from pitter.models import User


class UserListView(APIView):
    @classmethod
    @access_token_required
    @response_list_serializer(UserListGetResponse)
    @swagger_auto_schema(
        responses={
            HTTPStatus.OK.value: 'Success',
            HTTPStatus.UNAUTHORIZED.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Получение списка пользователей',
        operation_description='Получение списка всех пользователей',
    )
    def get(cls, request: Request) -> List[User]:
        """Make response containg a list of users"""
        user_list: List[User] = list(User.get_users().values('id', 'login', 'name'))
        return user_list
