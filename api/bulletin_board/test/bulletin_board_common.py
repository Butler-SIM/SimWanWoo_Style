from rest_framework.test import (
    APITestCase,
)
from api.accounts.models import User
from api.bulletin_board.models import BulletinBoard


class BulletinBoardTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email="test@test.com", password="")
        cls.board = BulletinBoard.objects.create(title="테스트 게시글1", contents="테스트 내용1", user=cls.user)
        cls.disabled_board = BulletinBoard.objects.create(title="미공개 게시글", contents="미공개",
                                                          is_display=False, user=cls.user)



