from django.urls import path

from src.api_client import views

urlpatterns: list = [
    path('speech_to_text', views.SpeechToTextView.as_view(), name='speech_to_text'),
]
