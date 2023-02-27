from rest_framework import serializers
from api.bulletin_board.models import BulletinBoard


class BulletinBoardListSerializer(serializers.ModelSerializer):
    """BulletinBoard 목록 Serializer"""

    class Meta:
        model = BulletinBoard
        fields = [
            "id",
            "title",
            "user",
            "is_display",
            "created_date",
        ]


class BulletinBoardDetailSerializer(serializers.ModelSerializer):
    """BulletinBoard 상세 Serializer"""

    class Meta:
        model = BulletinBoard
        fields = [
            "id",
            "title",
            "contents",
            "user",
            "is_display",
            "created_date",
        ]


class BulletinBoardCreateSerializer(serializers.ModelSerializer):
    """BulletinBoard Create Serializer"""

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BulletinBoard
        fields = [
            "id",
            "title",
            "contents",
            "user",
            "is_display",
            "created_date",
        ]

