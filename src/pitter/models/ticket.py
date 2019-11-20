from __future__ import annotations
from typing import Dict

from django.db import models
from django.db.models import QuerySet

from pitter.models.base import BaseModel


class Ticket(BaseModel):
    fake_id = models.CharField(max_length=50, default='')
    message = models.CharField(max_length=256)
    user_comment = models.TextField()

    def to_dict(self) -> Dict[str, str]:
        """Return dict containig data"""
        return dict(id=self.id, fake_id=self.fake_id, message=self.message, user_comment=self.user_comment,)

    @staticmethod
    def create_ticket(fake_id: str, message: str, user_comment: str) -> Ticket:
        """Create new ticket"""
        new_ticket: Ticket = Ticket.objects.create(fake_id=fake_id, message=message, user_comment=user_comment,)
        return new_ticket

    @staticmethod
    def get_tickets() -> QuerySet:
        """Get all tickets"""
        return Ticket.objects.find().order_by('created_at')
