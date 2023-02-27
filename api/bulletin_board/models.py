from django.db import models

from api.accounts.models import User


class BulletinBoard(models.Model):
    """
    BulletinBoard Model
    """

    title = models.CharField(max_length=100, null=True, blank=True)
    contents = models.TextField(blank=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    is_display = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sww_bulletin_board"
        ordering = ["-id"]

