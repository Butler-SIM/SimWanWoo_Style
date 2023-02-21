import re

from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    NumericPasswordValidator,
)

from api.accounts.models import User


class CustomPasswordValidator:
    """비밀번호 유효성 검사"""

    def __init__(self, max_length=32):
        self.max_length = max_length

    def get_validation_result(self, password):
        """비밀번호 유효성 검사
        상세 설명:
            비밀번호 유효성 검사 함수를 모두 실행하는 함수
        Args:
            password : 회원가입시 유저가 입력한 request_password
        Returns:
            성공시
            tuple:  (True, "validate_success")
            실패시
            tuple: (False, Message)
        Example:
            #>>> CustomPasswordValidator().get_validation_result(password)
        Note:
                -
        """
        MinimumLengthValidator().validate(password)
        NumericPasswordValidator().validate(password)

        if not self.hangul_validate(password)[0]:
            return self.hangul_validate(password)

        if not self.combination_validate(password)[0]:
            return self.combination_validate(password)

        if not self.max_length_validate(password)[0]:
            return self.max_length_validate(password)

        return True, "validate_success"

    def hangul_validate(self, password):
        """비밀번호 한글 유효성 검사
        상세 설명:
            request_password1에 한글이 있는지 검사하는 함수
        Args:
            password : 회원가입시 유저가 입력한 request_password
        Returns:
            성공시
            tuple:  (True, Message)
            실패시
            tuple: (False, Message)
        Example:
            #>>> CustomPasswordValidator.hangul_validation(password)
        Note:
            -
        """

        if re.search("^[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]", password):
            return False, {"hangul": "비밀번호에 한글이 포함되어 있습니다"}

        return True, "hangul_validation_success"

    def combination_validate(self, password):
        """비밀번호 조합 유효성 검사
        상세 설명:
            request_password1에 비밀번호 조합이 영문/숫자/특수문자 2가지이상 조합되어있는지 확인하는 함수
        Args:
            password : 회원가입시 유저가 입력한 request_password
        Returns:
            성공시
            tuple:  (True, Message)
            실패시
            tuple: (False, Message)
        Example:
            #>>> CustomPasswordValidator.combination_validate(password)
        Note:
            -
        """
        count = 0
        if re.search("[A-Za-z]", password):
            count += 1
        if re.search("[0-9]", password):
            count += 1
        if re.search("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》]", password):
            count += 1

        if count < 2:
            return False, {"combination": "비밀번호가 영문/숫자/특수문자중 2가지 이상으로 조합되지 않습니다"}
        return True, "combination_validation_success"

    def max_length_validate(self, password):
        """비밀번호 최대 길이 유효성 검사
        상세 설명:
            request_password1에 비밀번호 길이가 32자를 초과하는지 검사하는 함수
        Args:
            password : 회원가입시 유저가 입력한 request_password1
        Returns:
            성공시
            tuple:  (True, Message)
            실패시
            tuple: (False, Message)
        Example:
            #>>> CustomPasswordValidator.max_length_validate(password)
        Note:
            -
        """

        if len(password) > self.max_length:
            return False, {
                "max_length_validate": f"비밀번호 길이가 {self.max_length}자를 초과 하였습니다"
            }
        return True, "max_length_validate_success"


class NickNameValidator:
    """
    닉네임 유효성 검사 클래스
    """

    def __init__(self, min_length=3, max_length=8):
        self.min_length = min_length
        self.max_length = max_length
        self.message = ""

    def validate(self, nickname):
        """닉네임 유효성 검사
        상세 설명:
            닉네임 유효성 검사 함수를 모두 실행하는 함수
        Args:
            nickname : 유저가 입력한 request_nickname
        Returns:
            성공시
            tuple:  (True, "nickname validation success")
            실패시
            tuple: (False, Message)
        Example:
            #>>> NickNameValidator().duplicate_check(nickname)
        Note:
                -
        """
        if not self.duplicate_check(nickname)[0]:
            return False, self.message
        if not self.min_length_check(nickname)[0]:
            return False, self.message
        if not self.max_length_check(nickname)[0]:
            return False, self.message
        if not self.nickname_validate(nickname)[0]:
            return False, self.message

        self.message = "nickname validation success"
        return True, self.message

    def duplicate_check(self, nickname):
        """닉네임 중복 체크"""
        if User.objects.filter(nickname=nickname).exists():
            self.message = f"이미 존재하는 닉네임입니다"
            return False, self.message

        return True, self.message

    def min_length_check(self, nickname):
        """닉네임 최소 글자수 체크"""
        if len(nickname) < self.min_length:
            self.message = f"닉네임 글자수가 {self.min_length}보다 짧습니다"
            return False, self.message

        return True, self.message

    def max_length_check(self, nickname):
        """닉네임 최대 글자수 체크"""
        if len(nickname) > self.max_length:
            self.message = f"닉네임 글자수가 {self.max_length}보다 깁니다"
            return False, self.message

        return True, self.message

    def nickname_validate(self, nickname):
        if re.search("[^a-z|A-z|0-9|가-힣]", nickname):
            self.message = f"닉네임에 영문, 한글 숫자가 아닌 다른 문자가 포함되어 있습니다."
            return False, self.message

        return True, self.message
