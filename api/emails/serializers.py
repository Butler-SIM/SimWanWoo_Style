import uuid
import re
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import serializers
from api.accounts.models import User
from api.emails.models import VerificationEmail
from config import settings
from .tasks import email_send


class EmailSendSerializer(serializers.ModelSerializer):
    """
    이메일(인증코드)
    """

    class Meta:
        model = VerificationEmail
        fields = ["type", "email"]

    def create(self, validated_data):
        sender_email = settings.DEFAULT_FROM_EMAIL
        validated_data["code"] = re.sub(r"[^0-9]", "", str(uuid.uuid4()))[:6]
        validated_data["subject"] = "이메일 인증 코드 발송"
        message = "인증번호 : " + str(validated_data["code"])
        VerificationEmail.objects.create(**validated_data)

        context = {
            "code": validated_data["code"],
        }

        html_mail = render_to_string("code.html", context)

        # 메세지 보내기 celery 사용
        email_send.delay(
            validated_data["subject"],
            message,
            sender_email,
            [validated_data["email"]],
            html_message=html_mail,
        )
        # 메세지 보내기
        # email_send(
        #     validated_data["subject"],
        #     message,
        #     sender_email,
        #     [validated_data["email"]],
        #     html_message=html_mail,
        # )

        return validated_data


class EmailVerifySerializer(serializers.ModelSerializer):
    """
    이메일 인증코드 확인
    """

    class Meta:
        model = VerificationEmail
        fields = ["code", "email"]
