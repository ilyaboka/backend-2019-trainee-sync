from typing import Dict
from typing import Union

from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import FollowingRequest
from api_client.validation_serializers import FollowingResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_body_serializer
from pitter.decorators import request_query_parameters_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import Follower
from pitter.models import User
from pitter.utils import send_mail_in_new_thread


class FollowingView(APIView):
    @classmethod
    @access_token_required
    @request_query_parameters_serializer(FollowingRequest)
    @response_dict_serializer(FollowingResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        query_serializer=FollowingRequest,
        responses=dict(
            [
                FollowingResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.NotFoundError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Удаление подписки',
        operation_description='Отписаться от аккаунта другого пользователя',
    )
    def delete(cls, request: Request) -> Dict[str, Union[bool, str]]:
        """Удаление подписки"""
        unfollowing_id: str = request.query_params['id']
        try:
            unfollowing: User = User.objects.get(id=unfollowing_id)
        except User.DoesNotExist:
            raise exceptions.NotFoundError(f'User with id {unfollowing_id} not found')

        follower: User = request.token_user

        try:
            following: Follower = Follower.objects.get(follower=follower, following=unfollowing)
        except Follower.DoesNotExist as follower_does_not_exist:
            raise exceptions.NotFoundError(f'You not follow user with id {unfollowing_id}') from follower_does_not_exist

        following.delete()

        response: Dict[str, Union[bool, str]] = dict(follow=False, id=unfollowing_id)
        return response

    @classmethod
    @access_token_required
    @request_body_serializer(FollowingRequest)
    @response_dict_serializer(FollowingResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=FollowingRequest,
        responses=dict(
            [
                FollowingResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.NotFoundError.get_schema(),
                exceptions.ConflictError.get_schema(),
                exceptions.UnprocessableEntityError.get_schema(),
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
            raise exceptions.UnprocessableEntityError("You can't follow yourself")

        try:
            Follower.create_follower(follower, following)
        except IntegrityError as integrity_error:
            raise exceptions.ConflictError(f'You already follow user with id {following_id}') from integrity_error

        if following.email_notifications_enabled:
            send_mail_in_new_thread(
                f'User {follower.login} follows you',
                f'User {follower.login} follows you on Pitter',
                [following.email_address],
            )

        response: Dict[str, Union[bool, str]] = dict(follow=True, id=following_id)
        return response
