from django.contrib import admin

from core.forms import UserEntityCreationForm, UserEntityChangeForm
from .models import UserEntity


@admin.register(UserEntity)
class UserEntityAdmin(admin.ModelAdmin):
    add_form = UserEntityCreationForm
    form = UserEntityChangeForm
    model = UserEntity
