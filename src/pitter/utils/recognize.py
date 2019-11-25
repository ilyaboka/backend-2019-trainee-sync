from http import HTTPStatus

from requests import post
from requests.exceptions import RequestException

from pitter import exceptions
from pitter.settings import ASYNCHRONOUS_SERVICE_URL


def recognize(speech_file: bytes) -> str:
    """Вернуть распознанный текст из аудиофайла с речью"""
    try:
        recognized_rext: str = post(ASYNCHRONOUS_SERVICE_URL, data=speech_file).json()['recognizedText']
    except (RequestException, KeyError, ValueError) as exception:
        raise exceptions.PitterException("Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR.value) from exception
    return recognized_rext
