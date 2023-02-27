from api.comment.test.coment_common import CommentTestCase
from common.util import reverse_querystring


class CommentReadTestCase(CommentTestCase):
    comment_list_url = "comment:bulletin_board_comments-list"

    def test_get_board_comment_list_success(self):
        """인증된 사용자 게시판 댓글 목록 조회 성공"""
        list_url = reverse_querystring(
            self.comment_list_url, query_kwargs={"bulletin_board_id": self.board.id}
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        print("test_get_board_comment_list_success : ", response.data)

    def test_not_authorized_user_get_board_comment_list_success(self):
        """인증되지 않은 사용자 매거진 댓글 목록 조회 성공"""
        list_url = reverse_querystring(
            self.comment_list_url, query_kwargs={"bulletin_board_id": self.board.id}
        )
        self.client.force_authenticate()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, 200)
        print("test_not_authorized_user_get_board_comment_list_success : ", response.data)
