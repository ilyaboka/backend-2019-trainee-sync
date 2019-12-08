import logging
from smtplib import SMTPException
from threading import Thread
from typing import List

from django.conf import settings
from django.core.mail import send_mail

logger: logging.Logger = logging.getLogger(__name__)


def try_send_mail(subject: str, body: str, recipient_email_addresses: List[str]) -> None:
    """Отправить письмо, написать в log в случае ошибки"""
    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, recipient_email_addresses)
    except SMTPException as smtp_exception:
        logger.error('Fail to send email: %s', str(smtp_exception))


def send_mail_in_new_thread(subject: str, body: str, recipient_email_addresses: List[str]) -> None:
    """Отправить письмо в отдельном потоке, написать в log в случае ошибки"""
    Thread(target=try_send_mail, args=(subject, body, recipient_email_addresses)).start()
