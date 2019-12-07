from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class EmailPostRequest(serializers.Serializer):
    email: serializers.EmailField = serializers.EmailField(label='email пользователя')


class EmailPostResponse(ResponseSerializer):
    email: serializers.EmailField = serializers.EmailField(label='email пользователя')
