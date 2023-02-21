from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views.login import CustomLoginView, CustomLogOutView
from .views.password import CustomPasswordChangeView
from .views.signUp import CustomRegisterView, nickname_validation
from .views.social import KakaoLogin, GoogleLogin, AppleLogin
from .views.token import get_refresh_view, CustomTokenVerifyView
from .views.user import CustomUserDetailsView, my_liked_articles_count
from ..emails.views import VerificationCodeViewSet, MemberConfirmationViewSet

app_name = "accounts"
router = DefaultRouter()
router.register(r"profile", views.user.ProfileViewSet)
router.register(r"liked-articles", views.user.LikedArticleViewSet)

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
    # path(
    #     "profile-image",
    #     ProfileViewSet.as_view(
    #         {"put": "profile_image_update", "delete": "profile_image_delete"}
    #     ),
    # ),
    path("", include(router.urls)),
    # path("password/reset", CustomPasswordResetViewSet.as_view({"post": "post"})),
    # path(
    #     "password/reset/confirm",
    #     CustomPasswordResetConfirmViewSet.as_view({"post": "post"}),
    # ),
    path("token/refresh", get_refresh_view().as_view(), name="accounts_token_refresh"),
    path("token/verify", CustomTokenVerifyView.as_view(), name="accounts_token_verify"),
    path("user", CustomUserDetailsView.as_view(), name="accounts_user"),
    path(
        "member-confirmation",
        MemberConfirmationViewSet.as_view({"post": "create"}),
        name="accounts_member_confirmation",
    ),
    path(
        "liked-articles-count",
        my_liked_articles_count,
        name="accounts_liked_articles_count",
    ),
    # == social ==
    path("social/kakao/login", KakaoLogin.as_view(), name="accounts_kakao_login"),
    path("social/google/login", GoogleLogin.as_view(), name="accounts_google_login"),
    path("social/apple/login", AppleLogin.as_view(), name="accounts_apple_login"),
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
