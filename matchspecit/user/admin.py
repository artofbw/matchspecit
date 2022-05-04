from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(ModelAdmin):
    model = User


admin.site.register(User, UserAdmin)
