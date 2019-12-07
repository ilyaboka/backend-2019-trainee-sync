from rest_framework import serializers

from api_client.validation_serializers.response_serializer import ResponseSerializer


class EmailNotificationsEnabledPostRequest(serializers.Serializer):
    enabled: serializers.BooleanField = serializers.BooleanField(required=True, label='Флаг email уведомлений')


class EmailNotificationsEnabledGetResponse(ResponseSerializer):
    enabled: serializers.BooleanField = serializers.BooleanField(required=True, label='Флаг email уведомлений')
