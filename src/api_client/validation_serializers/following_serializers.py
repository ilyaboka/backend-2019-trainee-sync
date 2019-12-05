from rest_framework import serializers


class FollowingPostRequest(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )


class FollowingPostResponse(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта на который подписывается пользователь', max_length=256
    )
    success: serializers.BooleanField = serializers.BooleanField(required=True, label='Флаг подписки')
