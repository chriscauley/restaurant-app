from django.core.files.base import ContentFile
from django import forms
from django.contrib.auth import login
from django_registration.forms import RegistrationFormUniqueEmail
from django_registration.backends.activation.views import RegistrationView
import urllib

from server.user.models import User
from unrest import schema
from unrest.user.forms import SignUpForm, UserSettingsForm


@schema.register
class OwnerSignUpForm(SignUpForm):
    def save(self, commit=False):
        self.instance.role = 'owner'
        return super().save(commit=commit)


schema.unregister('UserSettingsForm')
@schema.register
class UserSettingsForm(UserSettingsForm):
    _avatar_url = None
    avatar_url = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('avatar_url') == self.instance.avatar_url:
            self._avatar_url = self.data.get('avatar_url')

    def clean_avatar_url(self):
        if self._avatar_url:
            response = urllib.request.urlopen(self._avatar_url['dataURL'])
            self._avatar_url['file'] = ContentFile(response.read())

    class Meta(UserSettingsForm.Meta):
        fields = ['username', 'avatar_url']