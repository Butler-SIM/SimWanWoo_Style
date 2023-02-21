from dj_rest_auth.jwt_auth import (
    CookieTokenRefreshSerializer,
    set_jwt_access_cookie,
    set_jwt_refresh_cookie,
)
from rest_framework_simplejwt.views import TokenVerifyView
from api.accounts.schemas import (
    TokenSchema,
)


@TokenSchema.verify_schema_view
class CustomTokenVerifyView(TokenVerifyView):
    """토큰확인"""


def get_refresh_view():
    """토큰 Refresh
    Returns a Token Refresh CBV without a circular import"""
    from rest_framework_simplejwt.settings import api_settings as jwt_settings
    from rest_framework_simplejwt.views import TokenRefreshView
    from django.utils import timezone

    @TokenSchema.refresh_schema_view
    class RefreshViewWithCookieSupport(TokenRefreshView):
        serializer_class = CookieTokenRefreshSerializer

        def finalize_response(self, request, response, *args, **kwargs):
            if response.status_code == 200 and "access" in response.data:
                set_jwt_access_cookie(response, response.data["access"])
                response.data["access_token_expiration"] = (
                    timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
                )

            if response.status_code == 200 and "refresh" in response.data:
                set_jwt_refresh_cookie(response, response.data["refresh"])
            return super().finalize_response(request, response, *args, **kwargs)

    return RefreshViewWithCookieSupport
