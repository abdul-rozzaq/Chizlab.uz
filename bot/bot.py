import telebot

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from .models import OTPCode
from .utils import generate_otp


User = get_user_model()

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    contact_button = KeyboardButton("📞 Raqamni yuborish", request_contact=True)

    markup.add(contact_button)

    bot.send_message(message.chat.id, "👋 Assalomu alaykum! Iltimos, ro'yxatdan o'tish uchun telefon raqamingizni yuboring:", reply_markup=markup)


@bot.message_handler(content_types=["contact"])
def handle_contact(message):

    contact = message.contact
    phone = contact.phone_number

    telegram_id = message.from_user.id

    user, created = User.objects.get_or_create(
        phone_number=phone,
        defaults={
            "telegram_id": telegram_id,
            "first_name": contact.first_name or "",
            "last_name": contact.last_name or "",
        },
    )

    if created:
        bot.send_message(message.chat.id, "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!")
    else:
        bot.send_message(message.chat.id, "📲 Siz allaqachon ro'yxatdan o'tgansiz.")

    bot.send_message(message.chat.id, "🔑 Yangi kod olish uchun /login ni bosing")


@bot.message_handler(commands=["login"])
def handle_login(message):

    user_id = message.from_user.id

    otp_obj, created = OTPCode.objects.get_or_create(telegram_id=user_id)

    if not created and otp_obj.is_expired():
        otp_obj.code = generate_otp()
        otp_obj.created_at = timezone.now()
        otp_obj.save()

        created = True

    if created:
        message_txt = "🔐 Sizning yangi tasdiqlash kodingiz: `%s`"
    else:
        message_txt = "🔐 Eski kod hali ham kuchda: `%s`"

    bot.send_message(message.chat.id, message_txt % otp_obj.code, parse_mode="Markdown")
