from django import forms
from django.shortcuts import render
from ..models import User
from django.http import HttpResponseRedirect
import bcrypt

def NewUserForm(request, error_message=None):
    form = UserForm()

    return render(request, 'new_user.html',
                  {'form': form,
                   'error_message': error_message})


def submit(request):
    new_user = User()

    new_user.user_name = request.POST['user_name']
    new_user.user_email = request.POST['user_email']
    new_user.user_phone_number = request.POST['user_phone']
    if not password_match(request):
        # TODO: return an error and repopulate form with recently entered data
        return HttpResponseRedirect('/user/new', request)
    new_user.user_salt = generate_salt()
    new_user.user_password_hash = protected(request, new_user)
    new_user.is_admin = False
    new_user.save()
    return HttpResponseRedirect('')


def password_match(request):
    if request.POST['user_pass'] == request.POST['user_pass1']:
        return True
    else:
        return False


def generate_salt():
    salt = bcrypt.gensalt()
    return salt


def protected(request, new_user):
    return bcrypt.hashpw(request.POST['user_pass'].encode('utf8'),
                         new_user.user_salt)


class UserForm(forms.Form):

    user_name = forms.CharField(label='Name:', max_length=127)
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_phone = forms.CharField(label='VOIP Extension:', max_length=15)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32)
    user_pass1 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:', max_length=32)

    def set_values(self, request):
        self.user_email.initial = request.POST['user_email']
        self.user_pass.initial = request.POST['user_pass']
        self.user_pass1.initial = request.POST['user_pass1']
        self.user_phone.initial = request.POST['user_phone']
        self.user_name.initial = request.POST['user_name']
