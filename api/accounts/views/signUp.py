from django.db import transaction
from dj_rest_auth.registration.views import RegisterView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.response import Response
from common.validation import NickNameValidator
from api.accounts.schemas import (
    NickNameSchema,
)
from api.accounts.schemas import SignUpSchema
from common.validation import CustomPasswordValidator



@SignUpSchema.signUp_schema
class CustomRegisterView(RegisterView):
    """회원 가입"""

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        # 비밀번호 유효성 검사
        validation_result = CustomPasswordValidator().get_validation_result(
            request.data["password1"]
        )
        if not validation_result[0]:
            return Response(
                validation_result[1],
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.save()
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


@NickNameSchema.nickname_validation_schema
@api_view(["POST"])
@permission_classes([AllowAny])
def nickname_validation(request, *args, **kwargs):
    """닉네임 유효성 검사"""
    validation_result, validation_message = NickNameValidator().validate(
        request.data["nickname"]
    )

    if not validation_result:
        return Response(
            {"validation_fail": validation_message},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {"validation_success": validation_message},
        status=status.HTTP_200_OK,
    )
