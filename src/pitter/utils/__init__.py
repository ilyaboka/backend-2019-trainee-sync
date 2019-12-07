from typing import List

from .mail import send_mail_in_new_thread
from .recognize import recognize

__all__: List[str] = [
    'recognize',
    'send_mail_in_new_thread',
]
