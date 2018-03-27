from django import forms
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from ..models import User
from .index import no_users
import bcrypt


def new_user_form(request, error_message=None):
    try:
        if not no_users():
            request.session["user_email"]
        if request.method == "GET":
            form = UserForm()
            return render(request, 'new_user.html',
                         {'form': form,
                           'error_message': error_message,
                           'success': False})
        else:
            return submit(request)
    except KeyError:
        return HttpResponseRedirect("../login")


def submit(request):
    new_user = User()

    new_user.user_name = request.POST['user_name']
    new_user.user_email = request.POST['user_email']
    new_user.user_phone_number = request.POST['user_phone']
    if not password_match(request):
        form = UserForm(initial={
            'user_name': request.POST['user_name'],
            'user_email': request.POST['user_email'],
            'user_phone': request.POST['user_phone']
        })
        return render(request, 'new_user.html', {
            'form': form,
            'error_message': 'Passwords do not match.',
            'success': False
        })
    new_user.user_salt = generate_salt()
    new_user.user_password_hash = protected(request, new_user)
    new_user.is_admin = False
    try:
        new_user.save()
    except IntegrityError:
        error_message = 'Account with email address \'' + \
                        str(request.POST['user_email'] +
                            '\' already exists.')
        form = UserForm(initial={
            'user_name': request.POST['user_name'],
            'user_email': request.POST['user_email'],
            'user_phone': request.POST['user_phone']
        })
        return render(request, 'new_user.html', {
            'form': form,
            'error_message': error_message,
            'success': False
        })
    return render(request, 'new_user.html', {
        'success': True
    })


def password_match(request):
    if request.POST['user_pass'] == request.POST['user_pass1']:
        return True
    else:
        return False


def generate_salt():
    salt = bcrypt.gensalt().decode('utf8')
    return salt


def protected(request, new_user):
    return bcrypt.hashpw(request.POST['user_pass'].encode('utf8'),
                         new_user.user_salt.encode('utf8')).decode('utf8')


class UserForm(forms.Form):
    user_name = forms.CharField(label='Name:', max_length=127)
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_phone = forms.CharField(label='VOIP Extension:', max_length=15)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32)
    user_pass1 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:', max_length=32)
