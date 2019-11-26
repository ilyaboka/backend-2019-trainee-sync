from http import HTTPStatus

import magic
from requests import post
from requests.exceptions import RequestException

from pitter import exceptions
from pitter.settings import ASYNCHRONOUS_SERVICE_URL


def recognize(speech_file: bytes) -> str:
    """Вернуть распознанный текст из аудиофайла с речью"""
    try:
        recognized_rext: str = post(
            ASYNCHRONOUS_SERVICE_URL,
            files=dict(speechFile=('speechFile', speech_file, magic.from_buffer(speech_file, mime=True,))),
        ).json()['recognizedText']
    except (RequestException, KeyError, ValueError) as exception:
        raise exceptions.PitterException("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR.value) from exception
    return recognized_rext
