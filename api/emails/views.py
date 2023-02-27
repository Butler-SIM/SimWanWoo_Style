from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.emails.models import VerificationEmail
from api.emails.schemas import AccountEmailSchema
from api.emails.serializers import EmailSendSerializer, EmailVerifySerializer


@AccountEmailSchema.account_email_schema_view
class VerificationCodeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = VerificationEmail.objects.all().order_by("-id")
    serializer_class = EmailSendSerializer

    @AccountEmailSchema.email_verify_schema
    def code_verify(self, request):
        """이메일 인증 코드 확인"""
        queryset = self.queryset.filter(
            email=request.data.get("email"), is_used=False
        ).first()

        if queryset.code != request.data.get("code"):
            return Response(
                {"message": "be not the same code"}, status=status.HTTP_400_BAD_REQUEST
            )

        queryset.is_used = True
        queryset.save()
        return Response({"message": "verified"}, status=status.HTTP_200_OK)

