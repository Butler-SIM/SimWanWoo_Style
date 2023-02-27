from rest_framework import serializers

from api.accounts.serializers.user import CommentUserProfileImageSerializer
from api.comment.models import Comment
from api.comment.serializers.reply import CommentReplyListSerializer


class CommentListSerializer(serializers.ModelSerializer):
    """ 댓글 목록 Serializer"""

    user = CommentUserProfileImageSerializer()
    comment_replies = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    reply_count = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = [
            "id",
            "comment",
            "user",
            "state",
            "comment_replies",
            "reply_count",
            "created_date",
        ]

    def get_comment(self, obj):
        """댓글 delete filter"""
        if obj.state == "DELETED":
            obj.user = None
            return "삭제된 댓글입니다"
        if obj.state == "SUSPENDED":
            obj.user = None
            return "관리자에 의해 삭제된 댓글입니다"
        return obj.comment

    def get_comment_replies(self, obj):
        """대댓글"""
        replies = [i for i in obj.bulletinboardcommentreplies]

        if replies:
            return CommentReplyListSerializer([replies[0]], many=True).data

        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    """ 댓글 생성 Serializer"""

    id = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ["id", "bulletin_board", "comment"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user

        return Comment.objects.create(**validated_data)


class CommentDetailSerializer(serializers.ModelSerializer):
    """ 댓글 상세 Serializer"""

    nickname = serializers.ReadOnlyField(source="user.nickname")

    class Meta:
        model = Comment
        fields = ["id", "comment", "nickname", "created_date", "updated_date"]


class CommentUpdateSerializer(serializers.ModelSerializer):
    """ 댓글 수정 Serializer"""

    class Meta:
        model = Comment
        fields = ["comment", "state"]

    def validate_state(self, value):
        if value == "SUSPENDED":
            raise serializers.ValidationError("not admin")

        return value

