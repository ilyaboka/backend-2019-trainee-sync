from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import MessagePostRequest
from api_client.validation_serializers import MessagePostResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import Message


class MessageView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @access_token_required
    @request_body_serializer(MessagePostRequest)
    @response_dict_serializer(MessagePostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=MessagePostRequest,
        responses=dict(
            [
                MessagePostResponse.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnsupportedMediaTypeError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Создание сообщения',
        operation_description='Создание сообщения',
    )
    def post(cls, request: Request) -> Dict[str, str]:
        """Создание сообщения"""
        new_message: Message = Message.create_message(request.token_user, request.data['audioMessageFile'])
        return dict(id=new_message.id, recognizedText=new_message.speech_transcript, user_id=new_message.user.id)
