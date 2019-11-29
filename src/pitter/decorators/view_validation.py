import functools
from typing import Any
from typing import Callable
from typing import Dict

from django.views.generic.base import View
from rest_framework.request import Request
from rest_framework.response import Response

from pitter.exceptions import exceptions


def request_post_serializer(serializer: type) -> Callable[[Callable], Callable]:
    """Валидация данных запроса"""

    def _decorator(handler: Callable[..., Response]) -> Callable[..., Response]:
        @functools.wraps(handler)
        def _wrapper(view: View, request: Request, *args: Any, **kwargs: Any) -> Response:
            ser = serializer(data=request.data)
            if not ser.is_valid():
                raise exceptions.ValidationError(message=str(ser.errors))
            return handler(view, request, *args, **kwargs)

        return _wrapper

    return _decorator


def response_dict_serializer(serializer: type) -> Callable[[Callable], Callable]:
    """Валидация данных ответа"""

    def _decorator(handler: Callable[..., Dict[str, Any]]) -> Callable[..., Response]:
        @functools.wraps(handler)
        def _wrapper(view: View, request: Request, *args: Any, **kwargs: Any) -> Response:
            response_data: Dict[str, Any] = handler(view, request, *args, **kwargs)
            ser = serializer(data=response_data)
            if not ser.is_valid():
                raise exceptions.ValidationError(message=str(ser.errors))
            return Response(ser.validated_data)

        return _wrapper

    return _decorator
