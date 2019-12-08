from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class FeedGetRequest(serializers.Serializer):
    page: serializers.IntegerField = serializers.IntegerField(required=True, label='Номер страницы', min_value=1)


class Message(serializers.Serializer):
    messageId: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор сообщения', max_length=256
    )
    speechTranscript: serializers.CharField = serializers.CharField(required=True, label='Распознанный текст')
    speechAudioFileURL: serializers.URLField = serializers.URLField(
        required=True, label='URL аудиофайла содержащего сообщение'
    )
    userId: serializers.CharField = serializers.CharField(
        required=True, label='Идентификатор аккаунта автора', max_length=256
    )


class FeedGetResponse(ResponseSerializer):
    messages: Message = Message(required=True, many=True)
    hasNextPage: serializers.BooleanField = serializers.BooleanField(required=True)
