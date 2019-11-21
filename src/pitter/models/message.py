from __future__ import annotations
from sys import stderr
from typing import Dict

from django.db import models
from django.db.models import QuerySet

from pitter.models.base import BaseModel
from pitter.integrations import GoogleSpeechToText
from pitter.integrations import GoogleSpeechToTextException


class Message(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    speech_audio_file_path = models.CharField(max_length=256)
    speech_transcript = models.TextField()

    def to_dict(self) -> Dict[str, str]:
        """Return dict containig data"""
        return dict(
            id=self.id,
            user=self.user,
            speech_audio_file_path=self.speech_audio_file_path,
            speech_transcript=self.speech_transcript,
        )

    @staticmethod
    def create_message(user: str, speech_audio_file_path: str) -> Message:
        """Create new message"""
        speech_transcript = None
        try:
            speech_transcript = GoogleSpeechToText.recognize(open(speech_audio_file_path).read())
        except GoogleSpeechToTextException:
            print(GoogleSpeechToTextException, file=stderr)
        new_message: Message = Message.objects.create(
            user=user, speech_audio_file_path=speech_audio_file_path, speech_transcript=speech_transcript,
        )
        return new_message

    @staticmethod
    def get_messages() -> QuerySet:
        """Get all message"""
        return Message.objects.find().order_by('created_at')
