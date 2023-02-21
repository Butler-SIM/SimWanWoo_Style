from rest_framework import serializers


class KakaoSerializer(serializers.Serializer):
    """카카오 Serializer"""

    access_token = serializers.CharField()


class AppleCallBackSerializer(serializers.Serializer):
    """애플 CallBack Serializer"""

    code = serializers.CharField()


class AppleSerializer(serializers.Serializer):
    """애플 Serializer"""

    code = serializers.CharField()
    id_token = serializers.CharField()
