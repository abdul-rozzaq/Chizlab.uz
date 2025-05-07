import json
import redis

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


from telebot.types import Update

from .bot import bot
from .models import OTPCode
from .serializers import OTPCodeSerializer

User = get_user_model()


class BotAuthView(GenericAPIView):
    serializer_class = OTPCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]

        otp = OTPCode.objects.filter(code=code).first()

        if not otp:
            return Response({"detail": "OTP does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if otp.is_expired():
            otp.delete()

            return Response({"detail": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(telegram_id=otp.telegram_id)

        except User.DoesNotExist:
            otp.delete()

            return Response({"detail": "User not registered"}, status=status.HTTP_400_BAD_REQUEST)

        otp.delete()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = Update.de_json(json.loads(request.body))

        bot.process_new_updates([update])

        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
