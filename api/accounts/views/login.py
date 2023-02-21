from dj_rest_auth.views import (
    LoginView,
    LogoutView,
)
from api.accounts.schemas import (
    LoginLogoutSchema,
)

@LoginLogoutSchema.login_schema_view
class CustomLoginView(LoginView):
    """로그인"""
    pass


@LoginLogoutSchema.logout_schema_view
class CustomLogOutView(LogoutView):
    """로그아웃"""
