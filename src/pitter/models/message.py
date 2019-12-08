from __future__ import annotations

from django.core.files.uploadedfile import UploadedFile
from django.db import models

from pitter.models.base import BaseModel
from pitter.utils import recognize


class Message(BaseModel):
    speech_audio_file: models.FileField = models.FileField()
    speech_transcript: models.TextField = models.TextField()
    user: models.ForeignKey = models.ForeignKey('User', on_delete=models.CASCADE)

    @staticmethod
    def create_message(user: str, speech_audio_file: UploadedFile) -> Message:
        """Создать новое сообщение"""
        new_message: Message = Message.objects.create(
            speech_audio_file=speech_audio_file, speech_transcript=recognize(speech_audio_file.read()), user=user
        )
        return new_message
