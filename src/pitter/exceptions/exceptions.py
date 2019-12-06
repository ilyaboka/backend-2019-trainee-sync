import traceback
from http import HTTPStatus
from typing import Optional
from typing import Tuple

from django.conf import settings
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.exceptions import APIException


class PitterException(APIException):
    default_detail: str = 'Something went wrong.'
    default_code: str = 'ServerError'
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(
        # pylint: disable=bad-continuation
        self,
        message: str,
        error_code: str,
        status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
    ) -> None:
        # pylint: enable=bad-continuation
        """Создать новое исключение"""
        detail = message
        super().__init__(detail, error_code)
        self.status_code: HTTPStatus = status_code

    @staticmethod
    def get_exception_serializer() -> type:
        """Вернуть serializer для исключений"""
        return ExceptionResponse

    # for ancestors
    @classmethod
    def get_schema(cls) -> Tuple[int, type]:
        """Вернуть пару код-serializer для исключений"""
        schema: Tuple[int, type] = (cls.status_code.value, ExceptionResponse)
        return schema

    def make_response(self) -> JsonResponse:
        """Создать response"""
        json_response: JsonResponse = JsonResponse(
            dict(code=self.get_codes(), message=str(self), debug=traceback.format_exc() if settings.DEBUG else None),
            status=self.status_code,
        )
        return json_response


class UnauthorizedError(PitterException):
    default_detail: str = 'Authorization error'
    status_code: HTTPStatus = HTTPStatus.UNAUTHORIZED

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)


class BadRequestError(PitterException):
    default_detail: str = 'Bad request error'
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)


class ConflictError(PitterException):
    default_detail: str = 'Conflict error'
    status_code: HTTPStatus = HTTPStatus.CONFLICT

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)


class ExceptionResponse(serializers.Serializer):
    code: serializers.CharField = serializers.CharField(required=True)
    message: serializers.CharField = serializers.CharField(required=True)
    debug: serializers.CharField = serializers.CharField(required=False, allow_null=True)


class InternalServerError(PitterException):
    default_detail: str = 'Internal server error'

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message and settings.DEBUG else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)


class NotFoundError(PitterException):
    default_detail: str = 'Not found'
    status_code: HTTPStatus = HTTPStatus.NOT_FOUND

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)


class UnsupportedMediaTypeError(PitterException):
    default_detail: str = 'Unsupported Media Type'
    status_code: HTTPStatus = HTTPStatus.UNSUPPORTED_MEDIA_TYPE

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)


class ValidationError(PitterException):
    default_detail: str = 'Validation error'
    status_code: HTTPStatus = HTTPStatus.UNPROCESSABLE_ENTITY

    def __init__(self, message: Optional[str] = None) -> None:
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        super().__init__(detail, exception_code, self.status_code)
