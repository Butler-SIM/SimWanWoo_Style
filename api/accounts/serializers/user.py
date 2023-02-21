from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from api.accounts.models import User
from common.aws import s3_move_temp_file, get_s3_obj_list
from common.validation import NickNameValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "marketing_check",
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


class UserProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "profile_image",
        ]

    def update(self, instance, validated_data):
        profile_image = validated_data["profile_image"]
        folder = self.context["profile_folder"]

        if profile_image not in get_s3_obj_list():
            raise ValidationError("There is no key in the bucket.")

        result, key = s3_move_temp_file(profile_image, folder)
        if not result:
            raise ValidationError("upload fail")

        instance.profile_image = key
        instance.save()

        return instance


class KeySerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
