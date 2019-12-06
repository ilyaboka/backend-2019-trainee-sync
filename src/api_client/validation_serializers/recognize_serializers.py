import magic
from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer
from pitter import exceptions


class RecognizePostRequest(serializers.Serializer):
    MAXIMAL_MAGIC_BYTE_LENGTH_FOR_ACCEPTED_FILETYPES: int = 12
    speechFile: serializers.FileField = serializers.FileField(
        required=True, label='Аудиофайл, содержащий речь для распознования'
    )

    @classmethod
    def validate_speechFile(cls, speech_file: UploadedFile) -> None:  # pylint: disable=invalid-name
        """Проверить mimetype - принимать только FLAC/WAVE файлы"""
        if magic.from_buffer(speech_file.read(cls.MAXIMAL_MAGIC_BYTE_LENGTH_FOR_ACCEPTED_FILETYPES), mime=True) not in [
            # pylint: disable=bad-continuation
            'audio/flac',
            'audio/x-wav',
        ]:
            # pylint: enable=bad-continuation
            raise exceptions.UnsupportedMediaTypeError('Invalid speech file')
        speech_file.open()


class RecognizePostResponse(ResponseSerializer):
    recognizedText = serializers.CharField(required=True, label='Распознанный текст')
