import json

from django.urls import reverse
from rest_framework.test import (
    APITestCase,
)

from api.accounts.models import User


class UserTestCase(APITestCase):
    user_update_url = reverse(
        "accounts:accounts_user",
    )
    email = "user@test.com"
    password = "qwer1234"

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)

    def test_user_nickname_update_success(self):
        """닉네임 변경 성공"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "nickname"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["nickname"], "nickname")
        print("test_user_nickname_update_success : ", response.data)

    def test_user_nickname_min_length_invalid(self):
        """닉네임 최소글자수 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "ni"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_min_length_invalid : ", response.data)

    def test_user_nickname_max_length_invalid(self):
        """닉네임 최대글자수 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)
        nickname = "T" * 9
        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": nickname}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_max_length_invalid : ", response.data)

    def test_user_nickname_special_characters_invalid(self):
        """닉네임 특수문자 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "닉네임!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_special_characters_invalid : ", response.data)

    def test_user_nickname_blank_invalid(self):
        """닉네임 공백 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "닉네임 공백"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_blank_invalid : ", response.data)

    def test_user_nickname_hangul_consonant_invalid(self):
        """닉네임 한글 자음이 포함 되어있는경우 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "닉네임자음ㄱ"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_hangul_consonant_invalid : ", response.data)

    def test_user_nickname_hangul_vowel_invalid(self):
        """닉네임 한글 모음이 포함 되어있는경우 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "닉네임모음ㅏ"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_hangul_vowel_invalid : ", response.data)

    def test_user_nickname_chinese_invalid(self):
        """닉네임 한문이 포함 되어있는경우 유효성 검사 실패"""
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.user_update_url,
            json.dumps({"nickname": "닉네임한문水"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("test_user_nickname_chinese_invalid : ", response.data)
