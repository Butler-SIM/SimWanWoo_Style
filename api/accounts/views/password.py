from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.response import Response
from api.accounts.models import User
from api.accounts.serializers.password import CustomPasswordChangeSerializer
from common.validation import CustomPasswordValidator
from api.accounts.schemas import (
    PasswordSchema,
)


@PasswordSchema.change_schema_view
class CustomPasswordChangeView(CreateAPIView):
    """비밀번호 변경"""

    serializer_class = CustomPasswordChangeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data.get("email"))
        password1 = request.data.get("new_password1")
        password2 = request.data.get("new_password2")
        # 비밀번호 유효성 검사
        validation_result = CustomPasswordValidator().get_validation_result(password1)
        if not validation_result[0]:
            return Response(
                validation_result[1],
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 비밀번호1과 비밀번호2가 동일하지 않을 때
        if password2 != password1:
            return Response(
                {"message": "not matched"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        # 비밀번호 설정
        user.set_password(password1)
        user.save()
        return Response(
            {"message": "changed"},
            status=status.HTTP_200_OK,
        )
