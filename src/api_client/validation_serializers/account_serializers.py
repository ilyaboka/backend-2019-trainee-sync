from rest_framework import serializers


class AccountDeleteRequest(serializers.Serializer):
    id: serializers.CharField = serializers.CharField(max_length=256)
