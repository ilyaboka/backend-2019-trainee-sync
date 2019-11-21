from django.urls import path

from api_client import views

urlpatterns: list = [
    path('delete_account', views.DeleteAccountView.as_view(), name='delete_account'),
    path('ticket', views.TicketMobileView.as_view(), name='ticket'),
    path('sign_up', views.SignUpView.as_view(), name='sign_up'),
    path('speech_to_text', views.SpeechToTextView.as_view(), name='speech_to_text'),
]
