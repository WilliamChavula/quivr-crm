from django import forms

from channel.models import Mode
from .models import Client

from core import validators


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "description",
            "preferred_communication",
            "phone",
            "social",
            "address",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name of lead"}),
            "email": forms.TextInput(attrs={"placeholder": "Enter email of lead"}),
            "description": forms.Textarea(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none",
                    "placeholder": "Describe lead",
                }
            ),
            "preferred_communication": forms.Select(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none",
                    "label": "Preferred Communication",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none"
                }
            ),
            "social": forms.TextInput(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none"
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none"
                }
            ),
        }

    def clean_preferred_communication(self):
        preferred_communication = self.cleaned_data["preferred_communication"]

        return validators.validate_preferred_communication_field(
            preferred_communication
        )

    def clean_phone(self):
        phone_value = self.cleaned_data["phone"]
        preferred_communication = self.cleaned_data["preferred_communication"]

        return validators.validate_phone_field(phone_value, preferred_communication)

    def clean_address(self):
        mail_value = self.cleaned_data["address"]
        preferred_communication = self.cleaned_data["preferred_communication"]

        return validators.validate_address_field(mail_value, preferred_communication)

    def clean_social(self):
        social_value = self.cleaned_data["social"]
        preferred_communication = self.cleaned_data["preferred_communication"]

        return validators.validate_social_field(social_value, preferred_communication)
