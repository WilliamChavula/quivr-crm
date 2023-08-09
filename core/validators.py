from typing import Optional
from django.forms import forms

from channel.models import Mode


def validate_preferred_communication_field(preferred_communication: Optional[str]):
    if preferred_communication is None:
        raise forms.ValidationError("Please select your preferred communication method")

    return preferred_communication


def validate_phone_field(
    phone_value: Optional[str], preferred_communication: Optional[str]
):
    if preferred_communication == Mode.Phone and not phone_value:
        raise forms.ValidationError(
            "You have selected phone as your preferred communication method but have not provided a phone number.\
             Please provide a phone number."
        )

    return phone_value


def validate_address_field(
    mail_value: Optional[str], preferred_communication: Optional[str]
):
    if preferred_communication == Mode.Mail and not mail_value:
        raise forms.ValidationError(
            "You have selected mail as your preferred communication method but have not provided a mailing address.\
             Please provide a mailing address."
        )

    return mail_value


def validate_social_field(
    social_value: Optional[str], preferred_communication: Optional[str]
):
    if preferred_communication == Mode.Social and not social_value:
        raise forms.ValidationError(
            "You have selected social media as your preferred communication but have not provided your social \
             media handle. Please provide your social media handle."
        )

    return social_value
