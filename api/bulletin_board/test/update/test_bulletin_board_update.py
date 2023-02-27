import json

from django.urls import reverse
from api.bulletin_board.test.bulletin_board_common import BulletinBoardTestCase


class BulletinBoardUpdateTestCase(BulletinBoardTestCase):
    update_url = "bulletin_board:bulletin_board-detail"

    def test_bulletin_board_title_update_success(self):
        """ Title update 성공"""
        self.client.force_authenticate(user=self.user)

        update_url = reverse(
            self.update_url, kwargs={"pk": self.board.id}
        )
        response = self.client.patch(
            update_url,
            json.dumps({"title": "update test"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "update title")
        print("test_bulletin_board_title_update_success : ", response.data)

    def test_bulletin_board_contents_update_success(self):
        """ contents update 성공"""
        self.client.force_authenticate(user=self.user)

        update_url = reverse(
            self.update_url, kwargs={"pk": self.board.id}
        )
        response = self.client.patch(
            update_url,
            json.dumps({"contents": "update contents"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "update contents")
        print("test_bulletin_board_contents_update_success : ", response.data)

    def test_bulletin_board_is_display_update_success(self):
        """ is_display update 성공"""
        self.client.force_authenticate(user=self.user)

        update_url = reverse(
            self.update_url, kwargs={"pk": self.disabled_board.id}
        )

        response = self.client.patch(
            update_url,
            json.dumps({"is_display": True}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["is_display"], True)
        print("test_bulletin_board_is_display_update_success : ", response.data)

    def test_not_author_bulletin_board_update(self):
        """작성자가 아닌 유저가 게시글 수정 시도"""
        self.client.force_authenticate(user=self.user)

        update_url = reverse(
            self.update_url, kwargs={"pk": self.disabled_board.id}
        )

        response = self.client.patch(
            update_url,
            json.dumps({"is_display": True}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        print("test_not_author_bulletin_board_update : ", response.data)
