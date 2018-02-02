from django import forms
from django.shortcuts import render
from django.http import HttpResponse


def submit(request):
    return HttpResponse("hello world")


class LoginForm(forms.Form):
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32)


def login(request, error_message=None):
    login_form = LoginForm()

    return render(request, 'new_user.html',
                  {'form': login_form,
                   'error_message': error_message})
