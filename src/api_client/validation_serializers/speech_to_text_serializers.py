from django.core.files.uploadedfile import UploadedFile
import magic
from rest_framework import serializers

from pitter.exceptions import ValidationError


class SpeechToTextPostRequest(serializers.Serializer):
    MAXIMAL_MAGIC_BYTES_LENGTH_FOR_ACCEPTED_FILETYPES: int = 12
    speechFile: serializers.FileField = serializers.FileField(required=True)

    @classmethod
    def validate_speechFile(cls, speech_file: UploadedFile) -> None:  # pylint: disable=C0103
        """ Check mimetype - accept only FLAC/WAVE files """
        mime_type: str = magic.from_buffer(
            speech_file.read(cls.MAXIMAL_MAGIC_BYTES_LENGTH_FOR_ACCEPTED_FILETYPES), mime=True
        )
        if mime_type not in ['audio/flac', 'audio/x-wav']:
            raise ValidationError('Invalid speech file', status_code=415)
        speech_file.open()


class SpeechToTextPostResponse(serializers.Serializer):
    recognizedText = serializers.CharField(required=True, label='Распознанный текст')
