from base64 import b64encode
from json import loads
from os import environ
from typing import Optional

from requests import Response
from requests.exceptions import RequestException
from requests import post

from pitter.exceptions import PitterException


class GoogleSpeechToTextException(PitterException):
    def __init__(
        # pylint: disable=C0330
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        payload: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        # pylint: enable=C0330
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        self.status_code: int = status_code if status_code else 500
        self.title: Optional[str] = title
        self.payload: Optional[str] = payload
        super().__init__(detail, exception_code)


class GoogleSpeechToText:
    URL: str = 'https://speech.googleapis.com/v1/speech:recognize'
    GOOGLE_API_KEY: str = environ['GOOGLE_API_KEY']

    @staticmethod
    def get_transcript_from_responce(responce: Response) -> str:
        """ Get transcript text from Google REST API Responce """
        try:
            transcript: str = loads(responce.text)['results'][0]['alternatives'][0]['transcript']
            return transcript
        except KeyError as key_error:
            raise GoogleSpeechToTextException(responce.text) from key_error

    @classmethod
    def recognize(cls, audio_file: bytes) -> str:
        """ Return transcript for speech in audiofile """
        try:
            return cls.get_transcript_from_responce(
                post(
                    cls.URL,
                    params=dict(key=cls.GOOGLE_API_KEY,),
                    json=dict(
                        audio=dict(content=b64encode(audio_file).decode('ascii'),), config=dict(languageCode='en-US',),
                    ),
                )
            )
        except (RequestException, UnicodeDecodeError) as exception:
            raise GoogleSpeechToTextException(str(exception)) from exception
