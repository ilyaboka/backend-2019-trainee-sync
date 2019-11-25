import functools
from http import HTTPStatus
from typing import Any
from typing import Callable
from typing import List

from django.views.generic.base import View
from jwt import decode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError
from rest_framework.request import Request
from rest_framework.response import Response

from pitter.exceptions import ValidationError
from pitter.settings import JSON_WEB_TOKEN_PUBLIC_KEY


def access_token_required(handler: Callable[..., Response]) -> Callable[..., Response]:
    """Проверка авторизации"""

    @functools.wraps(handler)
    def _wraper(view: View, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            auth: List[str] = request.META['HTTP_AUTHORIZATION'].split()
        except KeyError as key_error:
            raise ValidationError(
                'Authorization header expected', status_code=HTTPStatus.UNAUTHORIZED.value
            ) from key_error
        if auth[0] != 'Bearer':
            raise ValidationError(
                'Invalid authorization type: Bearer expected', status_code=HTTPStatus.UNAUTHORIZED.value
            )
        try:
            user_id: str = decode(auth[1], JSON_WEB_TOKEN_PUBLIC_KEY, algorithms=['RS256'])['id']
        except IndexError as index_error:
            raise ValidationError(
                'Invalid Authorization header', status_code=HTTPStatus.UNAUTHORIZED.value
            ) from index_error
        except ExpiredSignatureError as expire_signature_error:
            raise ValidationError(
                'Token expired', status_code=HTTPStatus.UNAUTHORIZED.value
            ) from expire_signature_error
        except (InvalidTokenError, KeyError) as exception:
            raise ValidationError('Invalid token', status_code=HTTPStatus.UNAUTHORIZED.value) from exception
        return handler(view, user_id, request, *args, **kwargs)

    return _wraper
