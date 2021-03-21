from django.core.files.base import ContentFile
from django import forms
from django.contrib.auth import login
from django_registration.forms import RegistrationFormUniqueEmail
from django_registration.backends.activation.views import RegistrationView
import urllib

from server import schema
from server.user.models import User


@schema.register('login')
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username and password:
            return self.cleaned_data
        user = User.objects.filter(username=username).first()
        if user:
            if user.check_password(password):
                self.user = user
                return self.cleaned_data
        raise forms.ValidationError("Username and password do not match")
    def save(self, commit=True):
        self.user.backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, self.user)

    user_can_GET = 'ANY'
    user_can_POST = 'ANY'


@schema.register('signup')
class SignupForm(RegistrationFormUniqueEmail):
    _role = 'user'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields.pop('password2')
    def clean(self, *args, **kwargs):
        self.cleaned_data['password2'] = self.cleaned_data.get('password1')
        super().clean()
    class Meta(RegistrationFormUniqueEmail.Meta):
        model = User
        fields = ['username', 'email', 'password1']

    def save(self, commit=False):
        user = super().save(commit=False)
        user.is_active = False
        user.role = self._role
        user.save()

        # Using django_registration's default view
        view = RegistrationView()
        view.request = self.request
        view.send_activation_email(user)
        return user

    user_can_GET = 'ANY'
    user_can_POST = 'ANY'

@schema.register('owner/signup')
class OwnerSignupForm(SignupForm):
    _role = 'owner'


@schema.register('settings')
class UserSettingsForm(forms.ModelForm):
    _avatar_url = None
    avatar_url = forms.CharField(required=False)

    user_can_POST = 'SELF'
    user_can_POST = 'SELF'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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