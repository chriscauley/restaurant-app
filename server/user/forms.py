from django import forms
from django.contrib.auth import login

from server import schema
from server.user.models import User


@schema.register
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
        login(self.request, self.user)