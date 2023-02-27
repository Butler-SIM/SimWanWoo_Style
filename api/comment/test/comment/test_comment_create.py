
import json
from django.urls import reverse

from api.comment.test.coment_common import CommentTestCase


class CommentCreateTestCase(CommentTestCase):
    comment_create_url = reverse(
        "comment:bulletin_board_comments-list",
    )

    def test_authorized_user_comment_create_success(self):
        """인증된 사용자 댓글 생성 성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.comment_create_url,
            json.dumps({"bulletin_board": self.board.id, "comment": "test comment create"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["comment"], "test comment create")
        print("test_authorized_user_comment_create_success : ", response.data)

    def test_authorized_user_comment_board_id_invalid(self):
        """인증된 사용자 댓글 생성 게시글 id 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.comment_create_url,
            json.dumps({"bulletin_board": 10000000, "comment": "test comment create"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["bulletin_board"][0],
            'Invalid pk "10000000" - object does not exist.',
        )
        print("test_authorized_user_comment_board_id_invalid : ", response.data)

    def test_authorized_user_comment_blank_invalid(self):
        """인증된 사용자 댓글 생성 comment 빈값 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.comment_create_url,
            json.dumps({"bulletin_board": self.board.id, "comment": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["comment"][0],
            "This field may not be blank.",
        )
        print("test_authorized_user_comment_blank_invalid : ", response.data)

    def test_authorized_user_comment_length_invalid(self):
        """인증된 사용자 댓글 생성 comment 글자수 유효성 검사 실패 (comment max_length = 500)"""
        comment = "T" * 501
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.comment_create_url,
            json.dumps({"bulletin_board": self.board.id, "comment": comment}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["comment"][0],
            "Ensure this field has no more than 500 characters.",
        )
        print("test_authorized_user_comment_length_invalid : ", response.data)

    def test_not_authorized_user_comment_create(self):
        """인증되지 않은 사용자가 댓글 생성 시도"""
        self.client.force_authenticate()
        response = self.client.post(
            self.comment_create_url,
            json.dumps({"bulletin_board": self.board.id, "comment": "test comment create"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        print("test_not_authorized_user_comment_create : ", response.data)
