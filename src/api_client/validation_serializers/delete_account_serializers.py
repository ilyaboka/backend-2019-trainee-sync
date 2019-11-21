from rest_framework import serializers


class DeleteAccountPostRequest(serializers.Serializer):
    login: serializers.CharField = serializers.CharField(max_length=32)
