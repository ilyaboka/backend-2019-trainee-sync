from rest_framework import serializers


class UserListGetRequest(serializers.Serializer):
    page: serializers.IntegerField = serializers.IntegerField(required=True, label='Номер страницы', min_value=1)


class User(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, label='Идентификатор аккаунта', max_length=256)
    login: serializers.CharField = serializers.CharField(required=True, label='Логин пользователя', max_length=32)
    name: serializers.CharField = serializers.CharField(
        required=True, allow_blank=True, label='Имя пользователя', max_length=32
    )


class UserListGetResponse(serializers.Serializer):
    users: User = User(required=True, many=True)
    hasNextPage: serializers.BooleanField = serializers.BooleanField(required=True)
