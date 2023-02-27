from django.urls import path, include
from api.bulletin_board.views.bulletin_board import BulletinBoardViewSet
from common.router import CustomSimpleRouter

app_name = "bulletin_board"
router = CustomSimpleRouter(trailing_slash=False)

router.register(r"", BulletinBoardViewSet, basename="bulletin_board")

urlpatterns = [
    path("", include(router.urls))
]
