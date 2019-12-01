from rest_framework import serializers


class UserListGetResponse(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, label='Идентификатор аккаунта', max_length=256)
    login: serializers.CharField = serializers.CharField(required=True, label='Логин пользователя', max_length=32)
    name: serializers.CharField = serializers.CharField(
        required=True, allow_blank=True, label='Имя пользователя', max_length=32
    )
