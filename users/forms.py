from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UserChangeForm as DjangoUserChangeForm
from .models import User


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("phone_number", "telegram_id")

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_unusable_password()

        if commit:
            user.save()

        return user


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ("phone_number", "telegram_id", "is_active", "is_staff")

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        return user
