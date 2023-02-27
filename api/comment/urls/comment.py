from django.urls import path, include
from api.comment.views.comment import CommentViewSet
from common.router import CustomSimpleRouter

app_name = "comment"
router = CustomSimpleRouter(trailing_slash=False)
router.register(r"", CommentViewSet, basename="bulletin_board_comments")

urlpatterns = [
    path("", include(router.urls)),
]
