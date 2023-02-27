from django.db.models import Prefetch, Count, Q
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from api.comment.models import Comment, CommentReply
from api.comment.schemas import CommentSchema
from api.comment.serializers.comment import CommentListSerializer, CommentCreateSerializer, CommentDetailSerializer, \
    CommentUpdateSerializer
from common.pagination import (
    BasePagination,
)

from rest_framework import viewsets, mixins
from common.permission import IsAuthorOrReadOnly


@CommentSchema.comment_schema_view
class CommentViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all().order_by("-id")
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer

        if self.action == "retrieve":
            return CommentDetailSerializer

        if self.action in ("update", "partial_update"):
            return CommentUpdateSerializer

        return CommentListSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ("update", "partial_update"):
            permission_classes = [IsAuthorOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = (
                self.queryset.prefetch_related(
                    Prefetch(
                        "bulletin_board_comment_replies",
                        queryset=CommentReply.objects.prefetch_related(
                            "user"
                        ).all(),
                        to_attr="bulletinboardcommentreplies",
                    ),
                    "user",
                )
                .annotate(
                    reply_count=Count(
                        "bulletin_board_comment_replies",
                        filter=Q(bulletin_board_comment_replies__state="ACTIVE"),
                    )
                )
                .filter(
                    Q(state="ACTIVE")
                    | Q(
                        state="DELETED",
                        bulletin_board_comment_replies__comment__isnull=False,
                        bulletin_board_comment_replies__state="ACTIVE",
                    )
                    | Q(
                        state="SUSPENDED",
                        bulletin_board_comment_replies__comment__isnull=False,
                        bulletin_board_comment_replies__state="ACTIVE",
                    )
                )
            )

        if self.action in ("update", "partial_update"):
            queryset = queryset.filter(state="ACTIVE")

        return queryset

