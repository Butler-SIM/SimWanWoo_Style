from django.urls import path, include

from api.comment.views.reply import CommentReplyViewSet
from common.router import CustomSimpleRouter

app_name = "comment-reply"
router = CustomSimpleRouter(trailing_slash=False)
router.register(
    r"",
    CommentReplyViewSet,
    basename="bulletin_board_comment_replies",
)

urlpatterns = [
    path("", include(router.urls)),
]
