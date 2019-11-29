from rest_framework import serializers


class SignInPostRequest(serializers.Serializer):
    login: serializers.CharField = serializers.CharField(required=True, label='Логин пользователя', max_length=32)
    password: serializers.CharField = serializers.CharField(
        required=True, label='Пароль пользователя', min_length=6, max_length=4096
    )


class SignInPostResponse(serializers.Serializer):
    token: serializers.CharField = serializers.CharField(required=True, label='Токен для доступа', max_length=1024)
