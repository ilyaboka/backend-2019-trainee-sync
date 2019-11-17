from base64 import b64encode
from json import loads
from os import environ

from requests import post
import magic

from src.pitter.exceptions import ValidationError

class GoogleSpeechToText:
    URL: str = 'https://speech.googleapis.com/v1/speech:recognize'
    GOOGLE_API_KEY: str = environ['GOOGLE_API_KEY']

    @classmethod
    def recognize(cls, audio_file: bytes) -> str:
        config = dict(languageCode='en-US',)

        mime_type = magic.from_buffer(audio_file, mime=True)

        if mime_type not in ['audio/flac', 'audio/x-wav']:
            raise ValidationError(message='Invalid speech file', status_code=415)


        return loads(
            post(
                cls.URL, params=dict(key=cls.GOOGLE_API_KEY,),
                json=dict(audio=dict(content=b64encode(audio_file).decode(),), config=config,)
            ).text
        )['results'][0]['alternatives'][0]['transcript']
