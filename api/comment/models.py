from django.db import models
from api.accounts.models import User
from api.bulletin_board.models import BulletinBoard

COMMENT_STATE = (
    ("ACTIVE", "ACTIVE"),
    ("DELETED", "DELETED"),
    ("SUSPENDED", "SUSPENDED"),
)


class Comment(models.Model):
    """
    Comment Model
    """

    comment = models.CharField(max_length=500, null=False, blank=False)
    bulletin_board = models.ForeignKey(
        BulletinBoard,
        null=False,
        on_delete=models.CASCADE,
        related_name="bulletin_board_comments",
        db_column="bulletin_board_id",
    )
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=COMMENT_STATE, default="ACTIVE")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sww_comment"
        ordering = ["-created_date"]

    def __str__(self):
        return self.comment


class CommentReply(models.Model):
    """
    Comment_Reply Model
    """

    comment = models.CharField(max_length=500, null=False)
    bulletin_board_comment = models.ForeignKey(
        Comment,
        null=False,
        on_delete=models.CASCADE,
        db_column="bulletin_board_comment_id",
        related_name="bulletin_board_comment_replies",
    )
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=COMMENT_STATE, default="ACTIVE")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sww_comment_reply"
        ordering = ["id"]
