import json
import uuid
import re
from datetime import datetime, date, timedelta
from rest_framework.test import (
    APITestCase,
)

from api.accounts.models import User
from api.emails.models import VerificationEmail


class SignUpTestCase(APITestCase):
    sign_up_url = "/api/accounts/signup"

    def setUp(self):
        self.sign_up_form = {
            "email": "test@test.com",
            "password1": "qwer1234!",
            "password2": "qwer1234!",
            "email_authentication_code": 0,
        }
        self.user = User.objects.create_user(email="user@test.com", password="")
        self.verification_email = VerificationEmail.objects.create(
            subject="슈퍼파인 인증 코드 발송",
            type="JOIN",
            email=self.sign_up_form["email"],
            code=re.sub(r"[^0-9]", "", str(uuid.uuid4()))[:6],
            is_used=True,
        )

    def tearDown(self):
        VerificationEmail.objects.all().delete()
        User.objects.all().delete()

    def test_sign_up_success(self):
        """회원가입 성공"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"]["email"], "test@test.com")
        print("test_sign_up_success : ", response.data)

    def test_invalid_email(self):
        """이메일 유효성 검사 실패"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        self.sign_up_form["email"] = "test"
        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")
        print("test_invalid_email : ", response.data)

    def test_duplicated_email(self):
        """이미 가입된 이메일이 있는경우"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        self.sign_up_form["email"] = self.user.email
        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["email"][0],
            "A user is already registered with this e-mail address.",
        )
        print("test_duplicated_email : ", response.data)

    def test_invalid_password_hangul(self):
        """비밀번호 한글 유효성 검사 실패"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        self.sign_up_form["password1"] = "비밀번호123abc"
        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["hangul"], "비밀번호에 한글이 포함되어 있습니다")
        print("test_invalid_password_hangul : ", response.data)

    def test_invalid_password_only_english_combination(self):
        """비밀번호 조합 비밀번호가 영어 만 일때 유효성 검사 실패"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        self.sign_up_form["password1"] = "password"
        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["combination"], "비밀번호가 영문/숫자/특수문자중 2가지 이상으로 조합되지 않습니다"
        )
        print("test_invalid_password_only_english_combination : ", response.data)

    def test_invalid_password_long_length(self):
        """비밀번호 길이가 32자 초과인 경우 유효성 검사 실패"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        password = "T" * 33
        self.sign_up_form["password1"] = password
        self.sign_up_form["password2"] = password

        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        print("test_invalid_password_long_length : ", response.data)

    def test_invalid_email_authentication_code_dose_not_exist(self):
        """이메일 인증코드가 존재하지 않는 경우"""
        self.client.force_authenticate()
        self.sign_up_form["email_authentication_code"] = 000000
        self.sign_up_form["password1"] = "123456789ab"
        self.sign_up_form["password2"] = "123456789ab"

        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["email_authentication_code"][0],
            "Email Authentication Code Dose Not Exist",
        )
        print("test_invalid_email_authentication_code_dose_not_exist : ", response.data)

    def test_invalid_email_authentication_not_used(self):
        """이메일 인증코드가 인증되지 않은경우"""
        self.client.force_authenticate()

        self.verification_email.is_used = False
        self.verification_email.save()

        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        self.sign_up_form["password1"] = "123456789ab"
        self.sign_up_form["password2"] = "123456789ab"

        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["email_authentication_code"][0],
            "Code not authenticated",
        )
        print("test_invalid_email_authentication_not_used : ", response.data)

    def test_invalid_email_authentication_expiration(self):
        """이메일 인증코드 생성후 3분이 지난경우(코드만료)"""
        self.client.force_authenticate()

        self.verification_email.created_date = (
            self.verification_email.created_date - timedelta(minutes=3)
        )
        self.verification_email.save()
        self.sign_up_form["email_authentication_code"] = self.verification_email.code
        self.sign_up_form["password1"] = "123456789ab"
        self.sign_up_form["password2"] = "123456789ab"

        response = self.client.post(
            f"{self.sign_up_url}",
            json.dumps(self.sign_up_form),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["email_authentication_code"][0],
            "Email Authentication Code Time Expiration",
        )
        print("test_invalid_email_authentication_expiration : ", response.data)
