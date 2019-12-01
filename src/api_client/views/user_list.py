from http import HTTPStatus
from typing import Dict
from typing import List
from typing import Union

from django.core.paginator import InvalidPage
from django.core.paginator import Page
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import UserListGetRequest
from api_client.validation_serializers import UserListGetResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_query_parameters_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import User


class UserListView(APIView):
    PAGE_SIZE: int = 16

    @classmethod
    @access_token_required
    @request_query_parameters_serializer(UserListGetRequest)
    @response_dict_serializer(UserListGetResponse)
    @swagger_auto_schema(
        query_serializer=UserListGetRequest,
        responses={
            HTTPStatus.OK.value: 'Success',
            HTTPStatus.UNAUTHORIZED.value: exceptions.ExceptionResponse,
            HTTPStatus.UNPROCESSABLE_ENTITY.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Получение списка пользователей',
        operation_description='Получение списка всех пользователей',
    )
    def get(cls, request: Request) -> Dict[str, Union[List[User], bool]]:
        """Make response containg a list of users"""

        paginator: Paginator = Paginator(User.get_users().values('id', 'login', 'name'), cls.PAGE_SIZE)
        page_number = request.query_params['page']

        try:
            page: Page = paginator.page(page_number)
        except InvalidPage as invalid_page:
            raise exceptions.ValidationError(f'Invalid page number: {page_number}') from invalid_page

        users: List[User] = list(page)
        has_next_page: bool = page.has_next()

        return dict(users=users, hasNextPage=has_next_page)
