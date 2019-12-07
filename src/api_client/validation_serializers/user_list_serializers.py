from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class UserListGetRequest(serializers.Serializer):
    login_search_string: serializers.CharField = serializers.CharField(
        required=False, label="Строка для поиска по login'у", max_length=32
    )
    page: serializers.IntegerField = serializers.IntegerField(label='Номер страницы', min_value=1)


class User(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(label='Идентификатор аккаунта', max_length=256)
    login: serializers.CharField = serializers.CharField(label='Логин пользователя', max_length=32)
    name: serializers.CharField = serializers.CharField(allow_blank=True, label='Имя пользователя', max_length=32)


class UserListGetResponse(ResponseSerializer):
    users: User = User(many=True)
    hasNextPage: serializers.BooleanField = serializers.BooleanField()
