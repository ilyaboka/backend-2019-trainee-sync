from rest_framework import serializers

from .response_serializer import ResponseSerializer


class FollowingPostRequest(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )


class FollowingPostResponse(ResponseSerializer):
    id: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )
    success: serializers.BooleanField = serializers.BooleanField(required=True, label='Флаг подписки')
