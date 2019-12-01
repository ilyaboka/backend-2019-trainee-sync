from __future__ import annotations

from typing import Dict

from django.db import models
from django.db.models import QuerySet

from pitter.models.base import BaseModel


class Follower(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    folower = models.ForeignKey('User', on_delete=models.CASCADE)

    def to_dict(self) -> Dict[str, str]:
        """Вернуть словарь данных"""
        return dict(id=self.id, user=self.user, folower=self.folower,)

    @staticmethod
    def create_follower(user: str, follower: str) -> Follower:
        """Создать нового подписчика"""
        new_follower: Follower = Follower.objects.create(
            user=user, follower=follower,
        )
        return new_follower

    @staticmethod
    def get_messages() -> QuerySet:
        """Вернуть всех подписчиков в порядке их создания"""
        return Follower.objects.find().order_by('created_at')
