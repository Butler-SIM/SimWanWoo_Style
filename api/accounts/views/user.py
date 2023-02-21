from dj_rest_auth.views import (
    UserDetailsView,
)
from api.accounts.schemas import (
    UserSchema,
)



@UserSchema.schema_view
class CustomUserDetailsView(UserDetailsView):
    """현재 인증된 사용자 조회, 수정"""



