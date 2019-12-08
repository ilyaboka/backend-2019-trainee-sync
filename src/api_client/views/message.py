from http import HTTPStatus
from typing import Dict
from typing import List

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import MessageDeleteRequest
from api_client.validation_serializers import MessagePostRequest
from api_client.validation_serializers import MessagePostResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_body_serializer
from pitter.decorators import request_query_parameters_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import Message
from pitter.utils import send_mail_in_new_thread


class MessageView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @access_token_required
    @request_query_parameters_serializer(MessageDeleteRequest)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        query_serializer=MessageDeleteRequest,
        responses=dict(
            [
                (HTTPStatus.NO_CONTENT.value, 'Success'),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.ForbiddenError.get_schema(),
                exceptions.NotFoundError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Удаление сообщения',
        operation_description='Удаление сообщения по id',
    )
    def delete(cls, request: Request) -> HttpResponse:
        """Удаление сообщения"""
        message_id: str = request.query_params['id']
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            raise exceptions.NotFoundError(f'Message with id: {message_id} not found')

        if message.user != request.token_user:
            raise exceptions.ForbiddenError("You can't delete other people messages")

        message.delete()
        response: HttpResponse = HttpResponse(status=HTTPStatus.NO_CONTENT.value)
        return response

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
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
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

        followers_mail_addresses: List[str] = [
            follow.follower.email_address
            for follow in request.token_user.followers.all()
            if follow.follower.email_notifications_enabled
        ]
        send_mail_in_new_thread(
            f'User {request.token_user.name} publish new message',
            f'{request.token_user.name} publish new message:\n'
            f'{new_message.speech_transcript}\n'
            f'{request.build_absolute_uri(new_message.speech_audio_file.url)}',
            followers_mail_addresses,
        )

        response: Dict[str, str] = dict(
            id=new_message.id, recognizedText=new_message.speech_transcript, user_id=new_message.user.id
        )
        return response
