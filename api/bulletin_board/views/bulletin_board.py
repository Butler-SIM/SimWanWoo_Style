
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
)

from api.bulletin_board.models import BulletinBoard
from api.bulletin_board.schemas import BulletinBoardSchema
from api.bulletin_board.serializers.bulletin_board import BulletinBoardDetailSerializer, BulletinBoardListSerializer, \
    BulletinBoardCreateSerializer
from common.pagination import BasePagination
from rest_framework import viewsets, mixins

from common.permission import IsAuthorOrReadOnly


@BulletinBoardSchema.article_schema_view
class BulletinBoardViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = BulletinBoard.objects.filter(is_display=True).order_by("-created_date")
    pagination_class = BasePagination
    filterset_fields = ["title"]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BulletinBoardDetailSerializer

        if self.action == "create":
            return BulletinBoardCreateSerializer

        return BulletinBoardListSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action == "create":
            permission_classes = [IsAuthenticated]

        if self.action in ("update", "partial_update", "destroy"):
            permission_classes = [IsAuthorOrReadOnly]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return super().create(request, *args, **kwargs)