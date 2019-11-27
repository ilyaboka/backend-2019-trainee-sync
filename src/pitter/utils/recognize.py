from typing import Any
from typing import Dict
from typing import Tuple

import magic
from requests import Response
from requests import post
from requests.exceptions import RequestException

from pitter import exceptions
from pitter.settings import ASYNCHRONOUS_SERVICE_URL


def recognize(speech_file: bytes) -> str:
    """Вернуть распознанный текст из аудиофайла с речью"""
    files: Dict[str, Tuple[str, bytes, str]] = dict(
        speechFile=('speechFile', speech_file, magic.from_buffer(speech_file, mime=True,)),
    )

    try:
        response: Response = post(ASYNCHRONOUS_SERVICE_URL, files=files)
    except RequestException as request_exception:
        raise exceptions.PitterException('Something went wrong', 'ServerError') from request_exception

    try:
        response_json: Dict[str, Any] = response.json()
    except ValueError as value_error:
        raise exceptions.PitterException('Something went wrong', 'ServerError') from value_error

    try:
        recognized_text: str = response_json['recognizedText']
    except KeyError as key_error:
        raise exceptions.PitterException('Something went wrong', 'ServerError') from key_error

    return recognized_text
