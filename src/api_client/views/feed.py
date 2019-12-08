from typing import Dict
from typing import List
from typing import Union

from django.core.paginator import InvalidPage
from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import FeedGetRequest
from api_client.validation_serializers import FeedGetResponse
from pitter import exceptions
from pitter.decorators import access_token_required
from pitter.decorators import request_query_parameters_serializer
from pitter.decorators import response_dict_serializer
from pitter.models import Message


class FeedView(APIView):
    PAGE_SIZE: int = 25

    @classmethod
    @access_token_required
    @request_query_parameters_serializer(FeedGetRequest)
    @response_dict_serializer(FeedGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        query_serializer=FeedGetRequest,
        responses=dict(
            [
                FeedGetResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.UnauthorizedError.get_schema(),
                exceptions.UnprocessableEntityError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Получение ленты подписок',
        operation_description='Получение ленты подписок',
    )
    def get(cls, request: Request) -> Dict[str, Union[List[Dict[str, str]], bool]]:
        """Make response containg a list of users"""
        feed_messages: QuerySet = Message.objects.filter(
            user__in=[follow.following for follow in request.token_user.following.all()] + [request.token_user]
        ).order_by('-created_at')

        paginator: Paginator = Paginator(feed_messages, cls.PAGE_SIZE)
        page_number = request.query_params['page']

        try:
            page: Page = paginator.page(page_number)
        except InvalidPage as invalid_page:
            raise exceptions.UnprocessableEntityError(f'Invalid page number: {page_number}') from invalid_page

        feed_messages_on_page: List[Dict[str, str]] = [
            dict(
                messageId=message.id,
                speechTranscript=message.speech_transcript,
                speechAudioFileURL=request.build_absolute_uri(message.speech_audio_file.url),
                userId=message.user.id,
            )
            for message in page
        ]
        has_next_page: bool = page.has_next()

        response: Dict[str, Union[List[Dict[str, str]], bool]] = dict(
            messages=feed_messages_on_page, hasNextPage=has_next_page
        )
        return response
