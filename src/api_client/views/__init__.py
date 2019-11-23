from typing import Sequence

from .account import AccountView
from .recognize import RecognizeView
from .signup import SignUpView
from .ticket import TicketMobileView

__all__: Sequence[str] = [
    'AccountView',
    'RecognizeView',
    'SignUpView',
    'TicketMobileView',
]
