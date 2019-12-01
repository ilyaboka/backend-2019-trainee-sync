from typing import Sequence

from .account import AccountView
from .recognize import RecognizeView
from .sign_in import SignInView
from .sign_up import SignUpView
from .ticket import TicketMobileView
from .user_list import UserListView

__all__: Sequence[str] = [
    'AccountView',
    'RecognizeView',
    'SignInView',
    'SignUpView',
    'TicketMobileView',
    'UserListView',
]
