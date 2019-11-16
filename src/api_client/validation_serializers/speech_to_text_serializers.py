from rest_framework import serializers


class SpeechToTextPostRequest(serializers.Serializer):
    speech_base64 = serializers.CharField(
        required=True,
        label='Речь для распознавания кодированная в base64'
    )


class SpeechToTextPostResponse(serializers.Serializer):
    recognized_text = serializers.CharField(required=True, label='Распознанный текст')
