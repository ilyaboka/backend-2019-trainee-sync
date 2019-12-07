import functools
from typing import Any
from typing import Callable

from django.views.generic.base import View
from rest_framework.request import Request
from rest_framework.response import Response

from pitter import exceptions


def access_token_required(handler: Callable[..., Response]) -> Callable[..., Response]:
    """Проверка авторизации"""

    @functools.wraps(handler)
    def _wraper(view: View, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.token_user:
            return handler(view, request, *args, **kwargs)
        raise exceptions.UnauthorizedError('Access token required')

    return _wraper
