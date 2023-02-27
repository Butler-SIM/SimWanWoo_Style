from api.comment.test.coment_common import ReplyTestCase
from common.util import reverse_querystring


class ReplyReadTestCase(ReplyTestCase):
    reply_list_url = "comment-reply:bulletin_board_comment_replies-list"

    def test_get_reply_list_success(self):
        """인증된 사용자 대댓글 목록 조회 성공"""
        reply_list_url = reverse_querystring(
            self.reply_list_url, query_kwargs={"bulletin_board_comment_id": self.comment.id}
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reply_list_url)
        self.assertEqual(response.status_code, 200)
        print("test_get_reply_list_success : ", response.data)

    def test_not_authorized_user_get_reply_list_success(self):
        """인증되지 않은 사용자 대댓글 목록 조회 성공"""
        reply_list_url = reverse_querystring(
            self.reply_list_url, query_kwargs={"bulletin_board_comment_id": self.comment.id}
        )
        self.client.force_authenticate()
        response = self.client.get(reply_list_url)
        self.assertEqual(response.status_code, 200)
        print("test_not_authorized_user_get_reply_list_success : ", response.data)
