from django.core.files.base import ContentFile
from django import forms
from django.contrib.auth import login
from django_registration.forms import RegistrationFormUniqueEmail
from django_registration.backends.activation.views import RegistrationView
import urllib

from server.user.models import User
from unrest import schema
from unrest.user.forms import SignUpForm


@schema.register
class OwnerSignUpForm(SignUpForm):
    def save(self, commit=False):
        self.instance.role = 'owner'
        return super().save(commit=commit)


@schema.register
class UserSettingsForm(forms.ModelForm):
    _avatar_url = None
    avatar_url = forms.CharField(required=False)

    user_can_GET = 'SELF'
    user_can_POST = 'SELF'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        if not self.data.get('avatar_url') == self.instance.avatar_url:
            self._avatar_url = self.data.get('avatar_url')

    def clean_avatar_url(self):
        if self._avatar_url:
            response = urllib.request.urlopen(self._avatar_url['dataURL'])
            self._avatar_url['file'] = ContentFile(response.read())
    def save(self, commit=True):
        instance = super().save(commit)
        if self._avatar_url:
            instance.avatar.save(self._avatar_url['name'], self._avatar_url['file'])
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'avatar_url']