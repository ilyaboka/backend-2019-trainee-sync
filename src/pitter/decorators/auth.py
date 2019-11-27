import functools
from http import HTTPStatus
from typing import Any
from typing import Callable
from typing import Dict
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
            authorization: str = request.META['HTTP_AUTHORIZATION']
        except KeyError as key_error:
            raise ValidationError(
                'Authorization header expected', status_code=HTTPStatus.UNAUTHORIZED.value
            ) from key_error

        authorization_parts: List[str] = authorization.split()
        if len(authorization_parts) != 2:
            raise ValidationError(
                'Invalid Authorization header: two parts expected', status_code=HTTPStatus.UNAUTHORIZED.value
            )

        if authorization_parts[0] != 'Bearer':
            raise ValidationError(
                'Invalid authorization type: Bearer expected', status_code=HTTPStatus.UNAUTHORIZED.value
            )

        token: str = authorization_parts[1]

        try:
            payload: Dict[str, Any] = decode(token, JSON_WEB_TOKEN_PUBLIC_KEY, algorithms=['RS256'])
        except ExpiredSignatureError as expire_signature_error:
            raise ValidationError(
                'Token expired', status_code=HTTPStatus.UNAUTHORIZED.value
            ) from expire_signature_error
        except InvalidTokenError as invalid_token_error:
            raise ValidationError('Invalid token', status_code=HTTPStatus.UNAUTHORIZED.value) from invalid_token_error

        try:
            user_id: str = payload['id']
        except KeyError as key_error:
            raise ValidationError('Invalid token', status_code=HTTPStatus.UNAUTHORIZED.value) from key_error

        return handler(view, user_id, request, *args, **kwargs)

    return _wraper
