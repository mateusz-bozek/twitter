# from django.forms import forms, ModelForm
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from workshop.models import Tweet


class AddTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['user']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Adres email')
    password = forms.CharField(max_length=40, widget=forms.PasswordInput, label='Hasło')

    def clean(self):

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(username=email, password=password)

        if user:
            self.cleaned_data['user'] = user
        else:
            raise ValidationError('Błędne dane logowania')


class AddCommentForm(forms.Form):
    ...
