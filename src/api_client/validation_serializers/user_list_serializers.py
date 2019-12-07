from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class UserListGetRequest(serializers.Serializer):
    login_search_string: serializers.CharField = serializers.CharField(
        required=False, label="Строка для поиска по login'у", max_length=32
    )
    page: serializers.IntegerField = serializers.IntegerField(required=True, label='Номер страницы', min_value=1)


class User(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, label='Идентификатор аккаунта', max_length=256)
    login: serializers.CharField = serializers.CharField(required=True, label='Логин пользователя', max_length=32)
    name: serializers.CharField = serializers.CharField(
        required=True, allow_blank=True, label='Имя пользователя', max_length=32
    )


class UserListGetResponse(ResponseSerializer):
    users: User = User(required=True, many=True)
    hasNextPage: serializers.BooleanField = serializers.BooleanField(required=True)
