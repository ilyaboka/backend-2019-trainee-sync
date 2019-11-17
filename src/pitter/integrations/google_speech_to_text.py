from base64 import b64encode
from json import loads
from os import environ

from requests import post

class GoogleSpeechToText:
    URL: str = 'https://speech.googleapis.com/v1/speech:recognize'
    GOOGLE_API_KEY: str = environ['GOOGLE_API_KEY']

    @classmethod
    def recognize(cls, audio_file: bytes) -> str:
        return loads(
            post(
                cls.URL, params=dict(key=cls.GOOGLE_API_KEY,),
                json=dict(
                    audio=dict(content=b64encode(audio_file).decode(),),
                    config=dict(languageCode='en-US',),
                )
            ).text
        )['results'][0]['alternatives'][0]['transcript']
