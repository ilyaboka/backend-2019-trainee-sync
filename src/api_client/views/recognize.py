from http import HTTPStatus
from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import RecognizePostRequest
from api_client.validation_serializers import RecognizePostResponse
from pitter import exceptions
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.utils import recognize


class RecognizeView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_body_serializer(RecognizePostRequest)
    @response_dict_serializer(RecognizePostResponse)
    @swagger_auto_schema(
        request_body=RecognizePostRequest,
        responses={
            HTTPStatus.OK.value: RecognizePostResponse,
            HTTPStatus.BAD_REQUEST.value: exceptions.ExceptionResponse,
            HTTPStatus.UNPROCESSABLE_ENTITY.value: exceptions.ExceptionResponse,
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Преобразование речи в текст',
        operation_description='Преобразование речи (FLAC, WAV) в текст с использованием асинхронного сервиса',
    )
    def post(cls, request: Request) -> Dict[str, str]:
        """Преобразование речи в текст с использованием асинхронного сервиса"""
        return dict(recognizedText=recognize(request.data['speechFile'].read()),)
