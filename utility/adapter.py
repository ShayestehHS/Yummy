from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.conf import settings
from termcolor import colored


class CustomAccountAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if email in settings.ACCOUNT_EMAIL_BLACKLIST:
            raise forms.ValidationError(f"{email} has been blacklisted")
        return super(CustomAccountAdapter, self).clean_email(email)