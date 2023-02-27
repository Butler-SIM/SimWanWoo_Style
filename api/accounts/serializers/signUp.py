from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

from api.emails.models import VerificationEmail


class CustomRegisterSerializer(RegisterSerializer):
    """회원가입 Serializer"""

    # nickname = serializers.CharField()
    # marketing_check = serializers.BooleanField()
    email_authentication_code = serializers.IntegerField()

    # def __int__(self, *args, **kwargs):
    #     """
    #     pop unnecessary_id
    #     """
    #     super(CustomRegisterSerializer, self).__init__(*args, **kwargs)
    #     self.fields.pop("username")

    def validate_email_authentication_code(self, email_authentication_code):
        # 이메일 인증 코드 확인

        try:
            verification_email = VerificationEmail.objects.get(
                code=email_authentication_code
            )
            if not verification_email.is_used:
                raise serializers.ValidationError(_("Code not authenticated"))

            code_expiration_time = verification_email.created_date + timedelta(
                minutes=3
            )
            if datetime.now() > code_expiration_time:
                raise serializers.ValidationError(
                    _("Email Authentication Code Time Expiration")
                )

        except VerificationEmail.DoesNotExist:
            raise serializers.ValidationError(
                _("Email Authentication Code Dose Not Exist")
            )


class NickNameSerializer(serializers.Serializer):
    """닉네임 유효성 검사 Serializer"""

    nickname = serializers.CharField()


class MemberConfirmationSerializer(serializers.Serializer):
    """회원 확인 Serializer"""

    email = serializers.EmailField()
