from http import HTTPStatus
from typing import Tuple

from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    @classmethod
    def get_schema(cls) -> Tuple[int, type]:
        """Вернуть пару код-serializer"""
        schema: Tuple[int, type] = (HTTPStatus.OK.value, cls)
        return schema
