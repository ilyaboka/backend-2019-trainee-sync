from typing import Dict
from uuid import uuid4

from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from api_client.validation_serializers import TicketPostRequest
from api_client.validation_serializers import TicketPostResponse
from pitter import exceptions
from pitter.decorators import request_body_serializer
from pitter.decorators import response_dict_serializer
from pitter.models.ticket import Ticket


class TicketMobileView(APIView):
    @classmethod
    @request_body_serializer(TicketPostRequest)
    @response_dict_serializer(TicketPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=TicketPostRequest,
        responses=dict(
            [
                TicketPostResponse.get_schema(),
                exceptions.BadRequestError.get_schema(),
                exceptions.InternalServerError.get_schema(),
            ],
        ),
        operation_summary='Создание заявки',
        operation_description='Создание заявки в сервисе Pitter',
    )
    def post(cls, request: Request) -> Dict[str, str]:
        """Создание заявки клиентом"""

        message: str = request.data['message']
        user_comment: str = request.data['userComment']
        fake_id: str = str(uuid4())

        result: Ticket = Ticket.create_ticket(
            fake_id=fake_id, message=message, user_comment=user_comment,
        )
        result_dict: dict = result.to_dict()

        return dict(
            id=result_dict["id"],
            fakeId=result_dict["fake_id"],
            message=result_dict["message"],
            userComment=result_dict["user_comment"],
        )
