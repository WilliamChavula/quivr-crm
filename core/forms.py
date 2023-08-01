from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class UserEntityCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class UserEntityChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
