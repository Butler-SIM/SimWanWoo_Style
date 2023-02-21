from rest_framework import serializers


class CustomPasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경 Serializer"""

    email = serializers.EmailField()
    new_password1 = serializers.CharField(min_length=8, write_only=True)
    new_password2 = serializers.CharField(min_length=8, write_only=True)
