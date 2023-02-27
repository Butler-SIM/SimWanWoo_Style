
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from api.comment.models import CommentReply
from api.comment.schemas import CommentReplySchema
from api.comment.serializers.reply import CommentReplyCreateSerializer, CommentReplyDetailSerializer, \
    CommentReplyUpdateSerializer, CommentReplyListSerializer
from common.pagination import (
    ReplyPagination,
)
from rest_framework import viewsets, mixins
from common.permission import IsAuthorOrReadOnly


@CommentReplySchema.comment_reply_schema_view
class CommentReplyViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CommentReply.objects.all()
    pagination_class = ReplyPagination

    def get_serializer_class(self):
        if self.action == "create":
            return CommentReplyCreateSerializer
        if self.action == "retrieve":
            return CommentReplyDetailSerializer
        if self.action in ("update", "partial_update"):
            return CommentReplyUpdateSerializer

        return CommentReplyListSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ("update", "partial_update"):
            permission_classes = [IsAuthorOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = self.queryset.prefetch_related(
                "user",
            )

        if self.action in ("update", "partial_update"):
            queryset = queryset.filter(state="ACTIVE")

        return queryset
