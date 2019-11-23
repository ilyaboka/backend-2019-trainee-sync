from http import HTTPStatus
from typing import Optional

from rest_framework import serializers
from rest_framework.exceptions import APIException


class ExceptionResponse(serializers.Serializer):
    code = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True)
    message = serializers.CharField(required=True)
    payload = serializers.DictField(required=False, allow_null=True)
    debug = serializers.CharField(required=False, allow_null=True)


class PitterException(APIException):
    default_detail: str = 'Something went wrong.'
    default_code: str = 'ServerError'

    def __init__(
        # pylint: disable=bad-continuation
        self,
        message: str,
        error_code: str,
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value,
    ) -> None:
        # pylint: enable=bad-continuation
        """Создать новое исключение"""
        detail = message
        super().__init__(detail, error_code)
        self.status_code = status_code

    @staticmethod
    def get_exception_serializer() -> type:
        """Вернуть serializer для исключений"""
        return ExceptionResponse


class ValidationError(PitterException):
    default_detail = 'Validation error'

    def __init__(
        # pylint: disable=bad-continuation
        self,
        message: Optional[str] = None,
        title: Optional[str] = None,
        payload: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        # pylint: enable=bad-continuation
        """Создать новое исключение"""
        detail: str = message if message else self.default_detail
        exception_code: str = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else HTTPStatus.UNPROCESSABLE_ENTITY
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)
