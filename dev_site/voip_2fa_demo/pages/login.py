from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import exceptions
from .new_user import protected
import random

from ..models import User


def submit(request):
    try:
        request.session['attempts'] += 1
        user_data = User.objects.get(user_email=request.session['user_email'])
        correct_code = user_data.user_2FA_code
        if request.POST['user_2fa_code'] == correct_code:
            request.session['login_complete'] = True
            del request.session['attempts']
            user_data.user_2FA_code = ""
            user_data.save()
            return HttpResponseRedirect("/")
        else:
            if request.session['attempts'] == 3:
                # ToDo: add logging here
                del request.session['attempts']
                del request.session['user_name']
                del request.session['user_email']
                del request.session['login_complete']
                user_data.user_2FA_code = ""
                user_data.save()
                return render(request, 'login.html', {
                    'form': LoginForm,
                    'error_message': "Two-factor authentication failed for user."
                })
            else:
                attempts_remaining = 3 - request.session['attempts']
                return render(request, "login.html", {
                    'form': TwoFaForm,
                    'error_message': "Code incorrect. Attempts remaining: " + str(attempts_remaining)
                })
    except KeyError:
        user_data = find_user(request)
        if type(user_data) == HttpResponse:
            return user_data

        password_check_response = check_password(user_data, request)
        if password_check_response is not None:
            return password_check_response
        request.session['user_name'] = user_data.user_name
        request.session['user_email'] = user_data.user_email
        request.session['login_complete'] = False
        request.session['attempts'] = 0
        generate_2fa_code(user_data)
        send_2fa_code()
        return render(request, "login.html", {
            "form": TwoFaForm,
            "error_message": None
        })


def find_user(request):
    try:
        user_data = User.objects.get(
            user_email=request.POST['user_email']
        )
        return user_data

    except exceptions.ObjectDoesNotExist:
        return render(request, "login.html", {
            "error_message": str("No user with email " +
                                 str(request.POST['user_email']) +
                                 " exists"),
            "form": LoginForm(initial={
                "user_email": request.POST['user_email']
            })
        })


def check_password(user_data, request):
    hashed_pw = protected(request, user_data)
    if hashed_pw != user_data.user_password_hash:
        return render(request, "login.html", {
            "error_message": "Password for user " +
                             str(request.POST['user_email']) +
                             " is incorrect",
            "form": LoginForm(initial={
                "user_email": request.POST['user_email']
            })
        })
    else:
        return None


def generate_2fa_code(user_data):
    # ToDo: ensure that method used to generate code is cryptographically random
    code = ""
    for i in range(6):
        code += str(random.SystemRandom().randint(0,9))
    user_data.user_2FA_code = code

    user_data.save()


def send_2fa_code():
    # ToDo: connect to voip program to send call
    pass


class LoginForm(forms.Form):
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32)


class TwoFaForm(forms.Form):
    user_2fa_code = forms.CharField(label='Validation code:', max_length=8)


def login(request):
    if request.method == 'GET':
        login_form = LoginForm()

        return render(request, 'login.html',
                      {'form': login_form,
                       'error_message': None
                       })
    else:
        return submit(request)
