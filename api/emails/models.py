from django.db import models


class VerificationEmail(models.Model):
    TYPE = (
        ("JOIN", "JOIN"),
        ("PASSWORD_CHANGE", "PASSWORD_CHANGE"),
    )
    subject = models.CharField(max_length=500, blank=True, null=True)
    code = models.IntegerField(default=1)
    type = models.CharField(max_length=20, choices=TYPE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_used = models.BooleanField(default=False)
    email = models.EmailField()

    class Meta:
        db_table = "sww_verification_emails"
        ordering = ["-created_date"]
