from django.urls import path

from api_client import views

urlpatterns: list = [
    path('ticket', views.TicketMobileView.as_view(), name='ticket'),
    path('speech_to_text', views.SpeechToTextView.as_view(), name='speech_to_text'),
]
