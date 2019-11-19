from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from api_client.validation_serializers import SpeechToTextPostRequest
from api_client.validation_serializers import SpeechToTextPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer
from pitter.decorators import response_dict_serializer
from pitter.integrations import GoogleSpeechToText


class SpeechToTextView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_post_serializer(SpeechToTextPostRequest)
    @response_dict_serializer(SpeechToTextPostResponse)
    @swagger_auto_schema(
        tags=["Pitter: mobile"],
        request_body=SpeechToTextPostRequest,
        responses={
            200: SpeechToTextPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Преобразование речи в текст',
        operation_description='Преобразование речи (FLAC, WAV) в текст с использованием Google Speech-To-Text',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Преобразование речи в текст с использованием Google Speech-To-Text
        :param request:
        :return:
        """
        recognized_text: str = GoogleSpeechToText.recognize(request.data['speechFile'].read())

        return dict(recognizedText=recognized_text,)
