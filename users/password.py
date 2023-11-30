from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import gettext
import re


from .models import User


class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Ваш пароль содержит менее 8 символов!"),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return "-Пароль должен состоять как минимум из 8 символов."


class AlphaValidator:
    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError(
                "Ваш пароль содержит только буквы!", code="alpha", params=None
            )
        if not (re.search(r"[A-Za-z]", password)):
            raise ValidationError("Ваш пароль не содержит букв!")

    def get_help_text(self):
        return "-Пароль не может содержать только буквы."


class DigitValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "Ваш пароль содержит только цифры!", code="digit", params=None
            )
        if not (re.search(r"[0-9]", password)):
            raise ValidationError("Ваш пароль не содержит цифр!")

    def get_help_text(self):
        return "-Пароль не может содержать только цифры."


class SymbolValidator:
    def validate(self, password, user=None):
        if not any([s in password for s in ["!", "@", "_", "&"]]):
            # if not("!" in password or "&" in password or "@" in password or "_" in password):
            raise ValidationError(
                "Ваш пароль не содержит спецсимволы!", code="digit", params=None
            )

    def get_help_text(self):
        return "-Пароль должен содержать спецсимволы(!, _, @, &)."


class RegisterValidator:
    def validate(self, password, user=None):
        if password.islower():
            raise ValidationError(
                "Ваш пароль содержит только символы нижнего регистра!",
                code="lower",
                params=None,
            )
        if password.isupper():
            raise ValidationError(
                "Ваш пароль содержит только символы верхнего регистра!",
                code="upper",
                params=None,
            )

    def get_help_text(self):
        return "-Пароль должен содержать символы верхнего и нижнего регистра."
