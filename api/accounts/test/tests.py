# import json
# from rest_framework.test import APITestCase
# from api.accounts.models import User
#
#
# SIGN_UP_FORM = {
#     "email": "test@test.com",
#     "nickname": "nicknametest",
#     "marketing_check": "0",
#     "password1": "qwer1234!",
#     "password2": "qwer1234!",
#     "phone_number": "01012345678",
#     "name": "TEST",
#     "gender": "m",
#     "birth_year": "2022",
#     "birth_day": "13",
# }
#
#
# class SignUpTestCase(APITestCase):
#     sign_up_url = "/api/accounts/signup"
#     email = "test@test.com"
#     password = "qwer1234!"
#
#     def setUp(self):
#         self.user = User.objects.create_user(email="test@test", password="qwer1234")
#
#     # def test_sign_up(self):
#     #     """테스트 회원가입"""
#     #     response = self.client.post(
#     #         self.sign_up_url,
#     #         json.dumps(SIGN_UP_FORM),
#     #         content_type="application/json",
#     #     )
#     #
#     #     self.token = response.data["access_token"]
#     #     self.assertEqual(response.status_code, 201)
#
#     def test_success(self):
#         pass
#
#     def test_required_email(self):
#         pass
#
#     def test_invalid_email(self):
#         pass
#
#     def test_duplicated_email(self):
#         pass
#
#
# class LoginTestCase(APITestCase):
#     def setUp(self):
#         self.sign_up_url = "/api/accounts/signup"
#         self.login_url = "/api/accounts/login"
#         self.email = "test@test.com"
#         self.password = "qwer1234!"
#
#         response = self.client.post(
#             self.sign_up_url,
#             json.dumps(SIGN_UP_FORM),
#             content_type="application/json",
#         )
#         self.token = response.data["access_token"]
#
#     def test_login(self):
#         """테스트 로그인"""
#         login_form = {
#             "email": self.email,
#             "password": self.password,
#         }
#         response = self.client.post(
#             self.login_url,
#             json.dumps(login_form),
#             content_type="application/json",
#         )
#         self.assertEqual(response.status_code, 200)
#
#
# class TokenTestCase(APITestCase):
#     def setUp(self):
#         self.sign_up_url = "/api/accounts/signup"
#         self.login_url = "/api/accounts/login"
#         self.token_verify_url = "/api/accounts/token/verify"
#         self.token_refresh_url = "/api/accounts/token/refresh"
#         self.email = "test@test.com"
#         self.password = "qwer1234!"
#
#         response = self.client.post(
#             self.sign_up_url,
#             json.dumps(SIGN_UP_FORM),
#             content_type="application/json",
#         )
#         self.access_token = response.data["access_token"]
#         self.refresh_token = response.data["refresh_token"]
#
#     def test_token_verify(self):
#         """테스트 토큰 확인"""
#         response = self.client.post(
#             self.token_verify_url,
#             json.dumps({"token": self.access_token}),
#             content_type="application/json",
#         )
#
#         self.assertEqual(response.status_code, 200)
#
#     def test_token_refresh(self):
#         """테스트 토큰 refresh"""
#         response = self.client.post(
#             self.token_refresh_url,
#             json.dumps({"refresh": self.refresh_token}),
#             content_type="application/json",
#         )
#
#         self.assertEqual(response.status_code, 200)
