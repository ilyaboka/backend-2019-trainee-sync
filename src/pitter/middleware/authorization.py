from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from django.conf import settings
from django.http import HttpResponse
from django.http.request import HttpRequest
from jwt import decode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError

from pitter import exceptions
from pitter.models.user import User


class AuthorizationMiddleware:
    def __init__(self, get_response: Callable):
        """Создать новый AuthMiddleware"""
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Проверить авторизацию и выполнить запрос"""
        response: HttpResponse

        if 'HTTP_AUTHORIZATION' not in request.META:
            request.token_user = None
            response = self.get_response(request)
            return response

        try:
            token_user: str = self.get_user(request.META['HTTP_AUTHORIZATION'])
        except exceptions.AuthorizationError as authorization_error:
            response = authorization_error.make_response()
            return response
        request.token_user = token_user

        response = self.get_response(request)
        return response

    @staticmethod
    def get_user(authorization: str) -> User:
        """Get user object from Authorization header"""
        authorization_parts: List[str] = authorization.split()

        if len(authorization_parts) != 2:
            raise exceptions.AuthorizationError('Invalid Authorization header: two parts expected')

        if authorization_parts[0] != 'Bearer':
            raise exceptions.AuthorizationError('Invalid authorization type: Bearer expected')

        token: str = authorization_parts[1]

        try:
            token_payload: Dict[str, Any] = decode(token, settings.JSON_WEB_TOKEN_PUBLIC_KEY, algorithms=['RS256'])
        except ExpiredSignatureError as expire_signature_error:
            raise exceptions.AuthorizationError('Token expired') from expire_signature_error
        except InvalidTokenError as invalid_token_error:
            raise exceptions.AuthorizationError('Invalid token') from invalid_token_error

        if 'id' not in token_payload:
            raise exceptions.AuthorizationError('Invalid token')

        user_id: str = token_payload['id']

        try:
            user: User = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthorizationError('Token user not found')

        return user
