from rest_framework import serializers

from .response_serializer import ResponseSerializer


class TicketPostRequest(serializers.Serializer):
    message = serializers.CharField(required=True, label='Сообщение')
    userComment = serializers.CharField(required=False, label='Комментарий пользователя', allow_null=True)


class TicketPostResponse(ResponseSerializer):
    id = serializers.CharField(required=True, label='Идентификатор заявки')
    fakeId = serializers.CharField(required=True, label='Фэйковый идентификатор заявки')
    message = serializers.CharField(required=True, label='Сообщение')
    userComment = serializers.CharField(required=False, label='Комментарий пользователя', allow_blank=True)
