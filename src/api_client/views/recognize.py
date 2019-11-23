from http import HTTPStatus
from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import RecognizePostRequest
from api_client.validation_serializers import RecognizePostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.integrations import GoogleSpeechToText


class RecognizeView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_post_serializer(RecognizePostRequest)
    @response_dict_serializer(RecognizePostResponse)
    @swagger_auto_schema(
        request_body=RecognizePostRequest,
        responses={
            HTTPStatus.OK.value: RecognizePostResponse,
            HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value: exceptions.ExceptionResponse,
            HTTPStatus.INTERNAL_SERVER_ERROR.value: exceptions.ExceptionResponse,
        },
        operation_summary='Преобразование речи в текст',
        operation_description='Преобразование речи (FLAC, WAV) в текст с использованием Google Speech-To-Text',
    )
    def post(cls, request: Request) -> Dict[str, str]:
        """Преобразование речи в текст с использованием Google Speech-To-Text"""
        recognized_text: str = GoogleSpeechToText.recognize(request.data['speechFile'].read())

        return dict(recognizedText=recognized_text,)
