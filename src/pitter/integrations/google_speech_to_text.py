from json import loads
from os import environ
from requests import post

class GoogleSpeechToText:
    URL: str = 'https://speech.googleapis.com/v1/speech:recognize'
    GOOGLE_API_KEY: str = environ['GOOGLE_API_KEY']

    @classmethod
    def recognize(cls, audio_base64: str) -> str:
        return loads(
            post(
                cls.URL, params=dict(key=cls.GOOGLE_API_KEY,),
                json=dict(audio=dict(content=audio_base64,), config=dict(languageCode='en-US',),)
            ).text
        )['results'][0]['alternatives'][0]['transcript']
