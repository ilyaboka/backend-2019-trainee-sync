from __future__ import annotations
from hashlib import pbkdf2_hmac
from os import urandom
from typing import Dict
from typing import Union

from django.db import models
from django.db.models import QuerySet

from pitter.models.base import BaseModel


class User(BaseModel):
    SALT_FOR_PASSWORD_LENGTH: int = 16
    PBKDF2_HMAC_HASH_NAME: str = 'sha256'
    PBKDF2_HMAC_NUMBER_OF_ITERATIONS: int = int(1e5)

    login = models.CharField(max_length=32)
    hash_of_password_with_salt = models.BinaryField(max_length=32)
    salt_for_password = models.BinaryField(max_length=SALT_FOR_PASSWORD_LENGTH)
    email_address = models.CharField(max_length=254, blank=True)
    email_notifications_enabled = models.BooleanField()
    name = models.CharField(max_length=32, blank=True)

    def to_dict(self) -> Dict[str, Union[bool, bytes, str]]:
        """Return dict containig data"""
        return dict(
            id=self.id,
            login=self.login,
            hash_of_password_with_salt=self.hash_of_password_with_salt,
            salt_for_password=self.salt_for_password,
            email_address=self.email_address,
            email_notifications_enabled=self.email_notifications_enabled,
            name=self.name,
        )

    @classmethod
    def create_user(cls, login: str, password: str) -> User:
        """Create new user"""
        salt_for_password = urandom(cls.SALT_FOR_PASSWORD_LENGTH)
        new_user: User = User.objects.create(
            login=login,
            hash_of_password_with_salt=pbkdf2_hmac(
                cls.PBKDF2_HMAC_HASH_NAME, password.encode(), salt_for_password, cls.PBKDF2_HMAC_NUMBER_OF_ITERATIONS
            ),
            salt_for_password=salt_for_password,
            email_notifications_enabled=False,
        )
        return new_user

    @staticmethod
    def get_users() -> QuerySet:
        """Get all users"""
        return User.objects.find().order_by('created_at')
