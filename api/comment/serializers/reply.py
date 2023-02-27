from rest_framework import serializers
from api.accounts.serializers.user import CommentUserProfileImageSerializer
from api.comment.models import CommentReply


class CommentReplyListSerializer(serializers.ModelSerializer):
    """ 대댓글 목록 Serializer"""

    user = CommentUserProfileImageSerializer()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = CommentReply
        fields = [
            "id",
            "comment",
            "user",
            "state",
            "created_date",
        ]

    def get_comment(self, obj):
        """대댓글 delete filter"""
        if obj.state == "DELETED":
            obj.user = None
            return "삭제된 댓글입니다"
        if obj.state == "SUSPENDED":
            obj.user = None
            return "관리자에 의해 삭제된 댓글입니다"
        return obj.comment


class CommentReplyCreateSerializer(serializers.ModelSerializer):
    """ 대댓글 생성 Serializer"""

    id = serializers.ReadOnlyField()

    class Meta:
        model = CommentReply
        fields = ["id", "bulletin_board_comment", "comment"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        return CommentReply.objects.create(**validated_data)


class CommentReplyDetailSerializer(serializers.ModelSerializer):
    """ 대댓글 상세 Serializer"""

    nickname = serializers.ReadOnlyField(source="user.nickname")

    class Meta:
        model = CommentReply
        fields = ["id", "comment", "nickname", "created_date", "updated_date"]


class CommentReplyUpdateSerializer(serializers.ModelSerializer):
    """ 대댓글 수정 Serializer"""

    class Meta:
        model = CommentReply
        fields = ["comment", "state"]

    def validate_state(self, value):
        if value == "SUSPENDED":
            raise serializers.ValidationError("not admin")
        return value
