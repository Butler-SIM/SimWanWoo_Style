import json

from django.urls import reverse

from api.bulletin_board.test.bulletin_board_common import BulletinBoardTestCase


class BulletinBoardCreateTestCase(BulletinBoardTestCase):
    create_url = reverse(
        "bulletin_board:bulletin_board-list",
    )

    def test_bulletin_board_create_success(self):
        """인증된 사용자 게시글 생성 성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.create_url,
            json.dumps({"title": "test", "contents": "test~"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        print("test_bulletin_board_create_success : ", response)

    def test_not_admin_bulletin_board_create(self):
        """인증되지 않은 사용자 게시글 생성 시도"""
        self.client.force_authenticate()
        response = self.client.post(
            self.create_url,
            json.dumps({"title": "test", "contents": "test~"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        print("test_not_admin_bulletin_board_create : ", response)
