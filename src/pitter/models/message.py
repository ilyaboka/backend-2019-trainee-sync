from __future__ import annotations

from typing import Dict

from django.db import models

from pitter.models.base import BaseModel
from pitter.utils import recognize


class Message(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    speech_audio_file_path = models.CharField(max_length=256)
    speech_transcript = models.TextField()

    def to_dict(self) -> Dict[str, str]:
        """Вернуть словарь с данными"""
        return dict(
            id=self.id,
            user=self.user,
            speech_audio_file_path=self.speech_audio_file_path,
            speech_transcript=self.speech_transcript,
        )

    @staticmethod
    def create_message(user: str, speech_audio_file_path: str) -> Message:
        """Создать новое сообщение"""
        speech_transcript = None
        speech_transcript = recognize(open(speech_audio_file_path).read())
        new_message: Message = Message.objects.create(
            user=user, speech_audio_file_path=speech_audio_file_path, speech_transcript=speech_transcript,
        )
        return new_message
