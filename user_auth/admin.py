from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    ordering = ('email',)
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
