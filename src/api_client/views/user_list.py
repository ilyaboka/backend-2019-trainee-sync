from typing import Dict
from typing import List
from typing import Union

from django.core.paginator import InvalidPage
from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
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
        tags=['Pitter: mobile'],
        query_serializer=UserListGetRequest,
        responses=dict(
            [
                UserListGetResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.NotFoundError.get_schema(),
                exceptions.UnprocessableEntityError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Получение списка пользователей',
        operation_description='Получение списка всех пользователей',
    )
    def get(cls, request: Request) -> Dict[str, Union[List[Dict[str, str]], bool]]:
        """Make response containg a list of users"""
        users: QuerySet = User.get_users().values('id', 'login', 'name')

        if 'loginSearchString' in request.query_params:
            users = users.filter(login__icontains=request.query_params['loginSearchString'])
            if not users:
                raise exceptions.NotFoundError(
                    f"Users with names containing {request.query_params['loginSearchString']} not found"
                )

        paginator: Paginator = Paginator(users, cls.PAGE_SIZE)
        page_number = request.query_params['page']

        try:
            page: Page = paginator.page(page_number)
        except InvalidPage as invalid_page:
            raise exceptions.UnprocessableEntityError(f'Invalid page number: {page_number}') from invalid_page

        users_on_page: List[Dict[str, str]] = list(page)
        has_next_page: bool = page.has_next()

        response: Dict[str, Union[List[Dict[str, str]], bool]] = dict(users=users_on_page, hasNextPage=has_next_page)
        return response
