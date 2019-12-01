import logging
import traceback
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.http.request import HttpRequest
from rest_framework.views import exception_handler

from pitter.exceptions import exceptions

LOGGER: logging.Logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        """Создать новый ErrorHandlerMiddleware"""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Выполнить запрос"""
        response: HttpResponse = self.get_response(request)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> Optional[JsonResponse]:
        # pylint: disable=no-self-use,unused-argument
        """Вернуть JsonResponse или None из exception"""
        if not isinstance(exception, exceptions.PitterException):
            LOGGER.exception(traceback.format_exc())
            return exceptions.InternalServerError(message=str(exception)).make_response()
        return None


def custom_exception_handler(exception: exceptions.PitterException, context: Dict[str, Any]) -> HttpRequest:
    """Обработчик ошибок"""
    response = exception_handler(exception, context)

    if settings.DEBUG:
        LOGGER.exception(traceback.format_exc())

    if isinstance(exception, AssertionError):
        return JsonResponse(
            dict(
                code='ValidationError',
                title='Ошибка валидации',
                message=str(exception),
                debug=traceback.format_exc() if settings.DEBUG else None,
            ),
            status=400,
        )

    if response is not None and hasattr(response, 'data'):
        if hasattr(response.data['detail'], 'code'):
            response.data['debug'] = traceback.format_exc() if settings.DEBUG else None
            response.data['code'] = response.data['detail'].code
            response.data['title'] = exception.payload if hasattr(exception, 'title') else None
            response.data['message'] = response.data['detail']
            response.data['payload'] = exception.payload if hasattr(exception, 'payload') else None
            del response.data['detail']

    return response
