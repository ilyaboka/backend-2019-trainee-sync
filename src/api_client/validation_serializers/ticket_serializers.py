from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class TicketPostRequest(serializers.Serializer):
    message = serializers.CharField(label='Сообщение')
    userComment = serializers.CharField(required=False, label='Комментарий пользователя', allow_null=True)


class TicketPostResponse(ResponseSerializer):
    id = serializers.CharField(label='Идентификатор заявки')
    fakeId = serializers.CharField(label='Фэйковый идентификатор заявки')
    message = serializers.CharField(label='Сообщение')
    userComment = serializers.CharField(required=False, label='Комментарий пользователя', allow_blank=True)
