from django.urls import path

from .views import telegram_webhook, BotAuthView

urlpatterns = [
    path("webhook/", telegram_webhook, name="telegram_webhook"),
    path("verify-otp/", BotAuthView.as_view(), name="verify-otp"),
]
