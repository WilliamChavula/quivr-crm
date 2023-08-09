from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from core.forms import UserEntityCreationForm
from .models import UserProfile


class SignUpView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
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
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, "userprofile/login.html")


class AccountView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        print(request.user.username)
        return render(request, "userprofile/account.html")
