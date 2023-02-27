from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)
from api.accounts.serializers.login import (
    LoginSerializer,
)
from api.accounts.serializers.password import CustomPasswordChangeSerializer
from api.accounts.serializers.signUp import (
    CustomRegisterSerializer,
    NickNameSerializer,
)
from api.accounts.serializers.social import KakaoSerializer

ACCOUNT_TAG = ["accounts"]
ACCOUNT_SOCIAL_TAG = ["accounts-social"]
ACCOUNT_MEMBER_CONFIRMATION_TAG = ["accounts-member-confirmation"]


class SignUpSchema:
    signUp_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"- 일반 회원가입 API_UPDATE : 2023-02-27",
        description="username은 제외하고 요청",
        request=CustomRegisterSerializer,
    )

    signUp_schema_view = extend_schema_view(post=signUp_schema)


class NickNameSchema:
    nickname_validation_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 닉네임 유효성 검사 API_UPDATE : 2023-02-27",
        request=NickNameSerializer,
    )


class LoginLogoutSchema:
    login_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 일반 로그인 API_UPDATE : 2023-02-27",
        request=LoginSerializer,
    )

    logOut_schema = extend_schema(
        tags=ACCOUNT_TAG, summary=f" - 로그아웃 API_UPDATE : 2023-02-27"
    )

    login_schema_view = extend_schema_view(post=login_schema)
    logout_schema_view = extend_schema_view(get=logOut_schema, post=logOut_schema)


class PasswordSchema:
    password_change_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 비밀번호 변경 API_UPDATE : 2023-02-27",
        request=CustomPasswordChangeSerializer,
    )

    password_reset_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 비밀번호 초기화 메일 보내기 API_UPDATE : 2023-02-27",
    )

    password_reset_confirm_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 비밀번호 변경 API_UPDATE : 2023-02-27",
    )

    change_schema_view = extend_schema_view(post=password_change_schema)
    reset_schema_view = extend_schema_view(post=password_reset_schema)
    reset_confirm_schema_view = extend_schema_view(post=password_reset_confirm_schema)


class TokenSchema:
    token_verify_schema = extend_schema(
        tags=ACCOUNT_TAG, summary=f" - 토큰 확인 API_UPDATE : 2023-02-27"
    )

    token_refresh_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 토큰 Refresh API_UPDATE : 2023-02-27",
    )

    verify_schema_view = extend_schema_view(post=token_verify_schema)
    refresh_schema_view = extend_schema_view(post=token_refresh_schema)


class UserSchema:
    detail_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 현재 인증된 사용자 정보 조회 API_UPDATE : 2023-02-27",
    )
    update_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"- 현재 인증된 사용자 정보 수정 API_UPDATE : 2023-02-27",
    )
    patch_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f" - 현재 인증된 사용자 정보 수정 API_UPDATE : 2023-02-27",
    )

    schema_view = extend_schema_view(
        get=detail_schema, put=update_schema, patch=patch_schema
    )




class SocialSchema:
    kakao_create_schema = extend_schema(
        tags=ACCOUNT_SOCIAL_TAG,
        summary=f" - 카카오 로그인, 회원가입 API_UPDATE : 2023-02-27",
        request=KakaoSerializer,
    )
    # google_create_schema = extend_schema(
    #     tags=ACCOUNT_SOCIAL_TAG,
    #     summary=f"{VERSION['V4']} - 구글 로그인, 회원가입 API_UPDATE : 2022-12-06",
    #     request=KakaoSerializer,
    # )

    # apple_create_schema = extend_schema(
    #     tags=ACCOUNT_SOCIAL_TAG,
    #     summary=f"{VERSION['V3']} - 애플 로그인, 회원가입 API_UPDATE : 2022-12-16",
    #     description="code, id_token 필요\n\n",
    #     request=AppleSerializer,
    # )

    kakao_schema_view = extend_schema_view(post=kakao_create_schema)
    # google_schema_view = extend_schema_view(post=google_create_schema)
    # apple_schema_view = extend_schema_view(post=apple_create_schema)



