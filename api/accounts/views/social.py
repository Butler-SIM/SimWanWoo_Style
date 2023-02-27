from allauth.socialaccount.providers.apple.client import AppleOAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from api.accounts.schemas import (
    SocialSchema,
)
from api.accounts.views.login import CustomLoginView
from config.settings import APPLE_RETURN_URL
from allauth.account.adapter import get_adapter


class CustomSocialLoginView(CustomLoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


@SocialSchema.kakao_schema_view
class KakaoLogin(CustomSocialLoginView):
    """카카오 로그인, 회원가입 Access_Token 필요"""

    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client


# @SocialSchema.google_schema_view
# class GoogleLogin(CustomSocialLoginView):
#     """구글 로그인, 회원가입 Access_Token 필요"""
#
#     adapter_class = GoogleOAuth2Adapter
#     client_class = OAuth2Client


# https://accounts.google.com/o/oauth2/v2/auth?
#     scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&
#     access_type=online&
#     include_granted_scopes=true&
#     response_type=code&
#     state=state_parameter_passthrough_value&
#     redirect_uri=http://localhost:8080/login&
#     client_id=998191296999-elarn2tgcn25uc3fs3m253qp3jcbodcd.apps.googleusercontent.com
#
# https://accounts.google.com/o/oauth2/v2/auth?
# client_id=998191296999-elarn2tgcn25uc3fs3m253qp3jcbodcd.apps.googleusercontent.com&
# response_type=token&
# redirect_uri=http://localhost:8080/login&
# scope=https://www.googleapis.com/auth/userinfo.email


# @SocialSchema.apple_schema_view
# class AppleLogin(CustomSocialLoginView):
#     """애플 로그인, 회원가입 Access_Token, id_token 필요"""
#
#     adapter_class = AppleOAuth2Adapter
#     client_class = AppleOAuth2Client
#     # Services IDs에서 설정한 return url 과 같아야함(https만 가능)
#     callback_url = APPLE_RETURN_URL
