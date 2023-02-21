import json

from django.urls import reverse
from rest_framework.test import (
    APITestCase,
)

from api.accounts.models import User


class LoginTestCase(APITestCase):
    login_url = reverse(
        "accounts:accounts_login",
    )
    email = "user@test.com"
    password = "qwer1234"

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(email=cls.email, password=cls.password)
        cls.not_active_user = User.objects.create_user(
            email="user2@test.com", password="qwer1234"
        )
        cls.not_active_user.is_active = False
        cls.not_active_user.save()

    def test_login_success(self):
        """로그인 성공"""
        response = self.client.post(
            self.login_url,
            json.dumps({"email": self.email, "password": self.password}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["email"], self.email)
        print("test_login : ", response.data)

    def test_invalid_email(self):
        """존재하지 않는 회원 로그인"""
        response = self.client.post(
            self.login_url,
            json.dumps({"email": "test@test.com", "password": self.password}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Unable to log in with provided credentials.",
        )
        print("test_invalid_email : ", response.data)

    def test_invalid_password(self):
        """비밀번호가 맞지 않는 경우"""
        response = self.client.post(
            self.login_url,
            json.dumps({"email": self.email, "password": "qqqq1111"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Unable to log in with provided credentials.",
        )
        print("test_invalid_password : ", response.data)

    def test_not_is_active(self):
        """비활성화 회원 로그인 시도"""
        response = self.client.post(
            self.login_url,
            json.dumps(
                {"email": self.not_active_user.email, "password": self.password}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Unable to log in with provided credentials.",
        )
        print("test_not_is_active : ", response.data)
