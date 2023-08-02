from django import forms

from .models import Lead


class LeadCreateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "name",
            "email",
            "description",
            "priority",
            "status",
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
            "priority": forms.Select(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none"
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "border border-slate-400 rounded-sm px-2 py-1 outline-none"
                }
            ),
        }
