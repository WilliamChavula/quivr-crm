from typing import Any

from django.shortcuts import render, redirect
from django.views.generic import View

from core.forms import UserEntityCreationForm
from .models import UserProfile


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = UserEntityCreationForm()
        context: dict[str:Any] = {"form": form}
        return render(request, "userprofile/signup.html", context)

    def post(self, request, *args, **kwargs):
        form = UserEntityCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)

            return redirect("accounts:login")

        return render(request, "userprofile/signup.html", {"form": form})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        # form =
        return render(request, "userprofile/login.html")
