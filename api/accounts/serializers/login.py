from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """로그인 Serializer"""

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
