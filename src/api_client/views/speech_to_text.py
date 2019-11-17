from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from src.api_client.validation_serializers import SpeechToTextPostRequest
from src.api_client.validation_serializers import SpeechToTextPostResponse
from src.pitter import exceptions
from src.pitter.decorators import request_post_serializer, response_dict_serializer
from src.pitter.integrations import GoogleSpeechToText


class SpeechToTextView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_post_serializer(SpeechToTextPostRequest)
    @response_dict_serializer(SpeechToTextPostResponse)
    @swagger_auto_schema(
        tags=["Pitter: audio"],
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

        recognized_text: str = GoogleSpeechToText.recognize(request.data['speech_file'].read())

        return dict(recognized_text=recognized_text,)
