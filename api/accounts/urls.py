from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views
from .views.login import CustomLoginView, CustomLogOutView
from .views.password import CustomPasswordChangeView
from .views.signUp import CustomRegisterView, nickname_validation
from .views.social import KakaoLogin
from .views.token import get_refresh_view, CustomTokenVerifyView
from .views.user import CustomUserDetailsView
from ..emails.views import VerificationCodeViewSet

app_name = "accounts"
router = DefaultRouter()

urlpatterns = [
    path(
        "signup",
        CustomRegisterView.as_view(),
        name="accounts_signup",
    ),
    path(
        "nickname-validation",
        nickname_validation,
        name="accounts_nickname_validation",
    ),
    path("login", CustomLoginView.as_view(), name="accounts_login"),
    path("logout", CustomLogOutView.as_view(), name="accounts_logout"),
    path(
        "password/change",
        CustomPasswordChangeView.as_view(),
        name="accounts_password_change",
    ),
    path("", include(router.urls)),
    path("token/refresh", get_refresh_view().as_view(), name="accounts_token_refresh"),
    path("token/verify", CustomTokenVerifyView.as_view(), name="accounts_token_verify"),
    path("user", CustomUserDetailsView.as_view(), name="accounts_user"),
    # == social ==
    path("social/kakao/login", KakaoLogin.as_view(), name="accounts_kakao_login"),
    # path("social/google/login", GoogleLogin.as_view(), name="accounts_google_login"),
    # path("social/apple/login", AppleLogin.as_view(), name="accounts_apple_login"),

    # ==emails==
    path(
        "email/send",
        VerificationCodeViewSet.as_view({"post": "create"}),
        name="accounts_email_send",
    ),
    path(
        "email/verify",
        VerificationCodeViewSet.as_view({"post": "code_verify"}),
        name="accounts_email_verify",
    ),

]
