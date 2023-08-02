from django import forms

from .models import Client


class ClientCreationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "email",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name of client"}),
            "email": forms.TextInput(attrs={"placeholder": "Enter email of client"}),
            "description": forms.Textarea(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none",
                    "placeholder": "Describe lead",
                }
            ),
        }
