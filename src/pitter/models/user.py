from __future__ import annotations

from hashlib import pbkdf2_hmac
from os import urandom
from typing import Dict
from typing import Union

from django.db import models
from django.db.models import QuerySet

from pitter.exceptions import PitterException
from pitter.models.base import BaseModel


class User(BaseModel):
    SALT_FOR_PASSWORD_LENGTH: int = 16
    PBKDF2_HMAC_HASH_NAME: str = 'sha256'
    PBKDF2_HMAC_NUMBER_OF_ITERATIONS: int = int(1e5)

    login = models.CharField(max_length=32, unique=True)
    hash_of_password_with_salt = models.BinaryField(max_length=32)
    salt_for_password = models.BinaryField(max_length=SALT_FOR_PASSWORD_LENGTH)
    email_address = models.CharField(max_length=254, blank=True)
    email_notifications_enabled = models.BooleanField()
    name = models.CharField(max_length=32, blank=True)

    @classmethod
    def create_user(cls, login: str, password: str) -> User:
        """Создать нового пользователя"""
        try:
            password_bytes = password.encode()
        except UnicodeError as unicode_error:
            raise PitterException('Error while encoding string', 'ServerError') from unicode_error

        salt_for_password = urandom(cls.SALT_FOR_PASSWORD_LENGTH)
        new_user: User = User.objects.create(
            login=login,
            hash_of_password_with_salt=pbkdf2_hmac(
                cls.PBKDF2_HMAC_HASH_NAME, password_bytes, salt_for_password, cls.PBKDF2_HMAC_NUMBER_OF_ITERATIONS,
            ),
            salt_for_password=salt_for_password,
            email_notifications_enabled=False,
        )
        return new_user

    @staticmethod
    def get_users() -> QuerySet:
        """Получить всех пользователей в порядке их создания"""
        return User.objects.all().order_by('created_at')

    def has_password(self, password: str) -> bool:
        """Проверить пароль пользователя"""
        try:
            password_bytes = password.encode()
        except UnicodeError as unicode_error:
            raise PitterException('Error while encoding string', 'ServerError') from unicode_error
        equals: bool = pbkdf2_hmac(
            self.PBKDF2_HMAC_HASH_NAME, password_bytes, self.salt_for_password, self.PBKDF2_HMAC_NUMBER_OF_ITERATIONS,
        ) == self.hash_of_password_with_salt.tobytes()  # pylint: disable=no-member
        return equals

    def to_dict(self) -> Dict[str, Union[bool, bytes, str]]:
        """Вернуть словарь с данными"""
        return dict(
            id=self.id,
            login=self.login,
            hash_of_password_with_salt=self.hash_of_password_with_salt,
            salt_for_password=self.salt_for_password,
            email_address=self.email_address,
            email_notifications_enabled=self.email_notifications_enabled,
            name=self.name,
        )
