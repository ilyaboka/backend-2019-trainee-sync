from rest_framework import serializers


class SignUpPostRequest(serializers.Serializer):
    login: serializers.CharField = serializers.CharField(max_length=32)
    password: serializers.CharField = serializers.CharField(min_length=6, max_length=4096)


class SignUpPostResponse(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(max_length=256)
    login: serializers.CharField = serializers.CharField(max_length=32)
