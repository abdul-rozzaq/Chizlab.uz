from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class CustomUserAdmin(DjangoUserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("get_full_name", "phone_number", "telegram_id", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff")

    search_fields = ("phone_number", "telegram_id")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("phone_number", "telegram_id", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("date_joined",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "last_name", "phone_number", "telegram_id", "is_active", "is_staff"),
            },
        ),
    )

    readonly_fields = ("date_joined",)

    def get_full_name(self, obj):
        return obj.get_full_name()

    get_full_name.short_description = "Full name"
