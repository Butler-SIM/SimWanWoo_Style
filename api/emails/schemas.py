from drf_spectacular.utils import extend_schema, extend_schema_view

from api.emails.serializers import EmailSendSerializer, EmailVerifySerializer

ACCOUNT_EMAIL_TAG = ["accounts-email"]


class AccountEmailSchema:
    email_send_schema = extend_schema(
        tags=ACCOUNT_EMAIL_TAG,
        summary=f" - 이메일 인증 코드 발송 API_UPDATE : 2023-02-25",
        description="이메일 인증 코드 발송\n\ntype - 회원가입 : join, 비밀번호 변경 : password_change ",
        request=EmailSendSerializer,
    )
    email_verify_schema = extend_schema(
        tags=ACCOUNT_EMAIL_TAG,
        summary=f" - 이메일 인증 코드 확인 API_UPDATE : 2023-02-25",
        request=EmailVerifySerializer,
    )

    account_email_schema_view = extend_schema_view(create=email_send_schema)
