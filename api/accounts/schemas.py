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
    MemberConfirmationSerializer,
)
from api.accounts.serializers.social import KakaoSerializer, AppleSerializer
from api.accounts.serializers.user import KeySerializer, UserProfileImageSerializer
from common.schemas import VERSION

ACCOUNT_TAG = ["api-accounts"]
ACCOUNT_SOCIAL_TAG = ["api-accounts-social"]
ACCOUNT_MEMBER_CONFIRMATION_TAG = ["api-accounts-member-confirmation"]


class SignUpSchema:
    signUp_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 일반 회원가입 API_UPDATE : 2022-11-16",
        description="username은 제외하고 요청",
        request=CustomRegisterSerializer,
    )

    signUp_schema_view = extend_schema_view(post=signUp_schema)


class NickNameSchema:
    nickname_validation_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 닉네임 유효성 검사 API_UPDATE : 2022-12-12",
        request=NickNameSerializer,
    )


class LoginLogoutSchema:
    login_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 일반 로그인 API_UPDATE : 2022-11-16",
        request=LoginSerializer,
    )

    logOut_schema = extend_schema(
        tags=ACCOUNT_TAG, summary=f"{VERSION['V4']} - 로그아웃 API_UPDATE : 2022-11-16"
    )

    login_schema_view = extend_schema_view(post=login_schema)
    logout_schema_view = extend_schema_view(post=logOut_schema)


class PasswordSchema:
    password_change_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 비밀번호 변경 API_UPDATE : 2022-12-02",
        request=CustomPasswordChangeSerializer,
    )

    password_reset_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 비밀번호 초기화 메일 보내기 API_UPDATE : 2022-11-18 !!사용X!!",
    )

    password_reset_confirm_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 비밀번호 변경 API_UPDATE : 2022-11-18 !!사용X!!",
    )

    change_schema_view = extend_schema_view(post=password_change_schema)
    reset_schema_view = extend_schema_view(post=password_reset_schema)
    reset_confirm_schema_view = extend_schema_view(post=password_reset_confirm_schema)


class ProfileSchema:

    profile_update_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 프로필 이미지 업데이트(presigned_url 업로드 성공후 요청) API_UPDATE : 2022-12-19",
        description="현재 인증된 토큰으로 사용자 프로필 이미지 업데이트\n\n" "presigned_url 업로드 성공후 요청 해주세요",
        request=KeySerializer,
        responses=UserProfileImageSerializer,
    )

    profile_delete_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 프로필 이미지 삭제 API_UPDATE : 2022-12-19",
        description="현재 인증된 토큰으로 사용자 프로필 이미지 삭제(DB=None, S3=delete)",
        request=[],
    )


class TokenSchema:
    token_verify_schema = extend_schema(
        tags=ACCOUNT_TAG, summary=f"{VERSION['V4']} - 토큰 확인 API_UPDATE : 2022-11-18"
    )

    token_refresh_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 토큰 Refresh API_UPDATE : 2022-11-18",
    )

    verify_schema_view = extend_schema_view(post=token_verify_schema)
    refresh_schema_view = extend_schema_view(post=token_refresh_schema)


class UserSchema:
    detail_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 현재 인증된 사용자 정보 조회 API_UPDATE : 2022-11-18",
    )
    update_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 현재 인증된 사용자 정보 수정 API_UPDATE : 2022-11-18",
    )
    patch_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - 현재 인증된 사용자 정보 수정 API_UPDATE : 2022-11-18",
    )

    schema_view = extend_schema_view(
        get=detail_schema, put=update_schema, patch=patch_schema
    )


class MemberConfirmation:
    create_schema = extend_schema(
        tags=[ACCOUNT_MEMBER_CONFIRMATION_TAG],
        summary=f"{VERSION['V4']} - 회원 확인 API_UPDATE : 2022-12-02",
        description="이메일을 요청하여 회원 확인하는 api입니다",
        request=MemberConfirmationSerializer,
    )
    schema_view = extend_schema_view(create=create_schema)


class SocialSchema:
    kakao_create_schema = extend_schema(
        tags=ACCOUNT_SOCIAL_TAG,
        summary=f"{VERSION['V4']} - 카카오 로그인, 회원가입 API_UPDATE : 2022-12-01",
        request=KakaoSerializer,
    )
    google_create_schema = extend_schema(
        tags=ACCOUNT_SOCIAL_TAG,
        summary=f"{VERSION['V4']} - 구글 로그인, 회원가입 API_UPDATE : 2022-12-06",
        request=KakaoSerializer,
    )

    apple_create_schema = extend_schema(
        tags=ACCOUNT_SOCIAL_TAG,
        summary=f"{VERSION['V3']} - 애플 로그인, 회원가입 API_UPDATE : 2022-12-16",
        description="code, id_token 필요\n\n",
        request=AppleSerializer,
    )

    kakao_schema_view = extend_schema_view(post=kakao_create_schema)
    google_schema_view = extend_schema_view(post=google_create_schema)
    apple_schema_view = extend_schema_view(post=apple_create_schema)


class LikedArticlesSchema:
    liked_articles_schema = extend_schema(
        tags=ACCOUNT_TAG,
        summary=f"{VERSION['V4']} - '좋아요'한 Article 리스트 API_UPDATE : 2023-01-10",
        description="'좋아요'한 Article 리스트",
    )

    liked_articles_schema_view = extend_schema_view(
        list=liked_articles_schema,
    )


liked_articles_schema = extend_schema(
    tags=ACCOUNT_TAG,
    summary=f"{VERSION['V4']} - '좋아요'한 아티클 수 조회 API_UPDATE : 2023-01-17",
)
