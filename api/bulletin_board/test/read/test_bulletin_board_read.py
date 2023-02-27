from django.urls import reverse

from api.bulletin_board.models import BulletinBoard
from api.bulletin_board.test.bulletin_board_common import BulletinBoardTestCase


class BulletinBoardReadTestCase(BulletinBoardTestCase):
    list_url = reverse(
        "bulletin_board:bulletin_board-list",
    )

    def test_get_bulletin_board_list_success(self):
        """인증된 사용자 게시판 조회 성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        print("test_get_bulletin_board_list_success : ", response.data)

    def test_get_bulletin_board_detail_success(self):
        """인증된 사용자 게시글 상세 조회 성공"""
        detail_url = reverse(
            "bulletin_board:bulletin_board-detail", kwargs={"pk": self.board.id}
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.board.id)
        print("test_get_bulletin_board_detail_success : ", response.data)

    def test_not_authorized_user_get_bulletin_board_list_success(self):
        """인증되지 않은 사용자 게시글 조회 성공"""
        self.client.force_authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        print("test_not_authorized_user_get_bulletin_board_list_success : ", response.data)

    def test_not_authorized_user_get_bulletin_board_detail_success(self):
        """인증되지 않은 사용자 게시글 상세 조회 성공"""
        article_detail_url = reverse(
            "bulletin_board:bulletin_board-detail", kwargs={"pk": self.board.id}
        )
        self.client.force_authenticate()

        response = self.client.get(article_detail_url)
        self.assertEqual(response.status_code, 200)
        print("test_not_authorized_user_get_bulletin_board_detail_success : ", response.data)
