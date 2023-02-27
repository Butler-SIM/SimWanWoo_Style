from django.urls import reverse
import json

from api.comment.test.coment_common import ReplyTestCase


class ReplyUpdateTestCase(ReplyTestCase):
    reply_detail_url = "comment-reply:bulletin_board_comment_replies-detail"

    def test_reply_author_update_success(self):
        """댓글 작성자가 대댓글 수정 성공"""
        self.client.force_authenticate(user=self.user)
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        response = self.client.patch(
            update_url,
            json.dumps({"comment": "comment update"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["comment"], "comment update")
        print("test_reply_author_update_success : ", response.data)

    def test_reply_author_update_blank_invalid(self):
        """댓글 작성자가 대댓글 수정 comment 빈값 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        response = self.client.patch(
            update_url,
            json.dumps({"comment": ""}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["comment"][0],
            "This field may not be blank.",
        )
        print("test_reply_author_update_blank_invalid : ", response.data)

    def test_reply_author_update_length_invalid(self):
        """댓글 작성자가 대댓글 수정 comment 글자수 유효성 검사 실패"""
        comment = "T" * 501
        self.client.force_authenticate(user=self.user)
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        response = self.client.patch(
            update_url,
            json.dumps({"comment": comment}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["comment"][0],
            "Ensure this field has no more than 500 characters.",
        )
        print("test_reply_author_update_length_invalid : ", response.data)

    def test_reply_author_delete_success(self):
        """댓글 작성자가 대댓글 삭제(state = DELETED 변경) 성공"""
        self.client.force_authenticate(user=self.user)
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        self.assertEqual(self.reply1.state, "ACTIVE")
        response = self.client.patch(
            update_url,
            json.dumps({"state": "DELETED"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], "DELETED")
        print("test_reply_author_delete_success : ", response.data)

    def test_reply_author_deleted_comment_delete(self):
        """대댓글 작성자가 이미 삭제 처리된 대댓글 삭제 시도"""
        self.client.force_authenticate(user=self.user)
        update_url = reverse(
            self.reply_detail_url, kwargs={"pk": self.deleted_reply.id}
        )
        self.assertEqual(self.deleted_reply.state, "DELETED")
        response = self.client.patch(
            update_url,
            json.dumps({"state": "DELETED"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        print("test_reply_author_deleted_comment_delete : ", response.data)

    def test_not_authorized_user_reply_update(self):
        """인증되지 않은 사용자가 대댓글 수정 시도"""
        self.client.force_authenticate()
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        response = self.client.patch(
            update_url,
            json.dumps({"state": "DELETED"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        print("test_not_authorized_user_reply_update : ", response.data)

    def test_not_authorized_user_reply_delete(self):
        """인증되지 않은 사용자가 대댓글 삭제 시도"""
        self.client.force_authenticate()
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        response = self.client.patch(
            update_url,
            json.dumps({"state": "DELETED"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        print("test_not_authorized_user_reply_delete : ", response.data)

    def test_not_author_user_reply_update(self):
        """작성자가 아닌 인증된 사용자가 대댓글 수정 시도"""
        self.client.force_authenticate(user=self.user2)
        update_url = reverse(self.reply_detail_url, kwargs={"pk": self.reply1.id})
        response = self.client.patch(
            update_url,
            json.dumps({"comment": "comment update"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        print("test_not_author_user_reply_update : ", response.data)
