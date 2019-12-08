import magic
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer
from pitter import exceptions


class MessageDeleteRequest(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(required=True, label='Идентификатор сообщения', max_length=256)


class MessagePostRequest(serializers.Serializer):
    MAXIMAL_MAGIC_BYTE_LENGTH_FOR_ACCEPTED_FILETYPES: int = 12
    audioMessageFile: serializers.FileField = serializers.FileField(
        required=True, label='Аудиофайл, содержащий голосовое сообщение'
    )

    @classmethod
    def validate_audioMessageFile(cls, audio_message_file: UploadedFile) -> None:  # pylint: disable=invalid-name
        """Проверить mimetype - принимать только FLAC/WAVE файлы"""
        if magic.from_buffer(
            # pylint: disable=bad-continuation
            audio_message_file.read(cls.MAXIMAL_MAGIC_BYTE_LENGTH_FOR_ACCEPTED_FILETYPES),
            mime=True,
        ) not in ['audio/flac', 'audio/x-wav']:
            # pylint: enable=bad-continuation
            raise exceptions.UnsupportedMediaTypeError('Invalid audio message file')
        audio_message_file.open()


class MessagePostResponse(ResponseSerializer):
    id: serializers.CharField = serializers.CharField(required=True, label='Идентификатор сообщения', max_length=256)
    speechTranscript = serializers.CharField(required=True, label='Распознанный текст')
