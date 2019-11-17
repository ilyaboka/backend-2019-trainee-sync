from rest_framework import serializers


class SpeechToTextPostRequest(serializers.Serializer):
    speech_file = serializers.FileField(required=True)


class SpeechToTextPostResponse(serializers.Serializer):
    recognized_text = serializers.CharField(required=True, label='Распознанный текст')
