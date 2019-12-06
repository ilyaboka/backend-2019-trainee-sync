from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class SignInPostRequest(serializers.Serializer):
    login: serializers.CharField = serializers.CharField(required=True, label='Логин пользователя', max_length=32)
    password: serializers.CharField = serializers.CharField(required=True, label='Пароль пользователя', max_length=4096)


class SignInPostResponse(ResponseSerializer):
    token: serializers.CharField = serializers.CharField(required=True, label='Токен для доступа', max_length=1024)
