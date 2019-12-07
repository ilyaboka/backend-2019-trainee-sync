from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class FollowingRequest(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(
        label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )


class FollowingResponse(ResponseSerializer):
    follow: serializers.BooleanField = serializers.BooleanField(label='Флаг подписки')
    id: serializers.CharField = serializers.CharField(
        label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )
