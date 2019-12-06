from typing import Dict
from typing import Union

from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import FollowingPostRequest
from api_client.validation_serializers import FollowingPostResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import Follower
from pitter.models import User


class FollowingView(APIView):
    @classmethod
    @access_token_required
    @request_body_serializer(FollowingPostRequest)
    @response_dict_serializer(FollowingPostResponse)
    @swagger_auto_schema(
        request_body=FollowingPostRequest,
        responses=dict(
            [
                FollowingPostResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.NotFoundError.get_schema(),
                exceptions.ConflictError.get_schema(),
                exceptions.ValidationError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Создание подписки',
        operation_description='Создание подписки на аккаунт другого пользователя',
    )
    def post(cls, request: Request) -> Dict[str, Union[bool, str]]:
        """Создание подписки"""
        following_id: str = request.data['id']
        try:
            following: User = User.objects.get(id=following_id)
        except User.DoesNotExist:
            raise exceptions.NotFoundError(f'User with id {following_id} not found')

        follower: User = request.token_user

        if follower == following:
            raise exceptions.ValidationError("You can't follow yourself")

        try:
            Follower.create_follower(follower, following)
        except IntegrityError as integrity_error:
            raise exceptions.ConflictError(f'You already follow user with id {following_id}') from integrity_error

        response: Dict[str, Union[bool, str]] = dict(id=following_id, success=True)
        return response
