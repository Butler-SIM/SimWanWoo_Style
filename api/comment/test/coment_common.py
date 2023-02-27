
from api.accounts.models import User
from api.bulletin_board.test.bulletin_board_common import BulletinBoardTestCase
from api.comment.models import Comment, CommentReply


class BoardTestCase(BulletinBoardTestCase):
    pass


class CommentTestCase(BoardTestCase):
    def setUp(self):
        super().setUp()
        self.user2 = User.objects.create_user(email="test2@test.com", password="")
        self.comment = Comment.objects.create(
            bulletin_board=self.board,
            comment="test comment",
            user=self.user,
        )
        self.deleted_comment = Comment.objects.create(
            bulletin_board=self.board,
            comment="deleted_comment",
            user=self.user,
            state="DELETED",
        )

    def tearDown(self):
        super().tearDown()
        Comment.objects.all().delete()


class ReplyTestCase(CommentTestCase):
    def setUp(self):
        super().setUp()
        self.reply1 = CommentReply.objects.create(
            bulletin_board_comment=self.comment,
            comment="reply test",
            user=self.user,
        )
        self.reply2 = CommentReply.objects.create(
            bulletin_board_comment=self.comment,
            comment="reply test22",
            user=self.user,
        )
        self.deleted_reply = CommentReply.objects.create(
            bulletin_board_comment=self.comment,
            comment="deleted reply",
            user=self.user,
            state="DELETED",
        )

    def tearDown(self):
        super().tearDown()
        CommentReply.objects.all().delete()
