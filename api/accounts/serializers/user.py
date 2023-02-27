from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from api.accounts.models import User
from common.validation import NickNameValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "nickname",
            "profile_image",
            "email",
            "is_superuser",
            "is_staff",
            "name",
            "phone_number",
        ]

    def validate_nickname(self, nickname):
        validation_result, validation_message = NickNameValidator().validate(nickname)
        if not validation_result:
            raise serializers.ValidationError(validation_message)

        return nickname


class CommentUserProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.FileField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "profile_image",
        ]