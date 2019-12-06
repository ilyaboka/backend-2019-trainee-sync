from rest_framework import serializers

from .response_serializer import ResponseSerializer


class FollowingRequest(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )


class FollowingResponse(ResponseSerializer):
    follow: serializers.BooleanField = serializers.BooleanField(required=True, label='Флаг подписки')
    id: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )
