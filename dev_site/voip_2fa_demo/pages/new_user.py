from django import forms
from django.db import IntegrityError
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from ..models import User
from .index import no_users
import bcrypt


def new_user_form(request, error_message=None):
    """
         Django page handler for user/new
    """
    try:
        if not no_users():
            # if users not in database, then it is possible to be logged in
            request.session["user_email"]
            # if user_email is set, user is logged in
        if request.method == "GET":
            form = UserForm()
            return render(request, 'new_user.html',
                          {'form': form,
                           'error_message': error_message,
                           'success': False})
            # displays the user creation form
        else:
            # method is post
            return submit(request)
            # handle form data
    except KeyError:
        # if not logged in
        return HttpResponseRedirect(reverse("login"))
        # redirect to log in page


def submit(request):
    """
        handles form data
    """
    new_user = User()

    new_user.user_name = request.POST['user_name']
    new_user.user_email = request.POST['user_email']
    new_user.user_phone_number = request.POST['user_phone']

    # create new user object and begin storing information
    if not password_match(request):
        # if confirmation password and password don't match
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
        # return to user creation form with error
    new_user.user_salt = generate_salt()
    new_user.user_password_hash = protected(request, new_user)
    new_user.is_admin = False
    try:
        new_user.save()
        # save new user to database
    except IntegrityError:
        # if user with email address already exists
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
        # display form with error message
    return render(request, 'new_user.html', {
        'success': True
    })
    # display page with success message


def password_match(request):
    """
        returns true if both passwords in form match
    """
    if request.POST['user_pass'] == request.POST['user_pass1']:
        return True
    else:
        return False


def generate_salt():
    """
        uses bcrypt to generate salt for password hashing
    """
    salt = bcrypt.gensalt().decode('utf8')
    return salt


def protected(request, new_user):
    """
        takes given password from form and the user's salt
        to hash the password
    """
    return bcrypt.hashpw(request.POST['user_pass'].encode('utf8'),
                         new_user.user_salt.encode('utf8')).decode('utf8')


class UserForm(forms.Form):
    """
        Django form that holds the fields to present in templates/new_user
    """
    user_name = forms.CharField(label='Name:', max_length=127)
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_phone = forms.CharField(label='VOIP Extension:', max_length=15)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32)
    user_pass1 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:', max_length=32)
