from __future__ import annotations

from django.db import models
from django.db.models import F
from django.db.models import Q

from pitter.models.base import BaseModel
from pitter.models.user import User


class Follower(BaseModel):
    follower = models.ForeignKey(User, models.CASCADE, 'following')
    following = models.ForeignKey(User, models.CASCADE, 'followers')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='uniqueness_of_follower-following_pair'),
            models.CheckConstraint(check=~Q(follower__exact=F('following')), name='forbid to follow yourself'),
        ]

    @staticmethod
    def create_follower(follower: User, following: User) -> Follower:
        """Создать нового подписчика"""
        new_follower: Follower = Follower.objects.create(follower=follower, following=following)
        return new_follower
