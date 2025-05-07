from django.db import models
from .utils import generate_otp
from django.utils import timezone
from datetime import timedelta


class OTPCode(models.Model):
    telegram_id = models.CharField("Telegram ID", max_length=32, unique=True)
    code = models.CharField("OTP Code", max_length=16, default=generate_otp)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP(telegram-id={self.telegram_id}, code={self.code})"
