# Register your models here.
from django.contrib import admin
from .models import User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

from django.contrib.auth import get_user_model
User = get_user_model()
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_active',
        'last_login',
        'date_joined'
    )

    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
