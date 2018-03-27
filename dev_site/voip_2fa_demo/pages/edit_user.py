from ..models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.db import IntegrityError
from .new_user import password_match, generate_salt, protected


def edit_user(request, user_id):
    """
    Django page handler for https traffic to /user/$id
    """
    try:
        if request.session["user_email"]:
            # if logged in
            if request.method == "GET":
                try:
                    user = User.objects.get(user_id=user_id)
                    # grab information for given id, then pre-populate a form with the values
                    form = UserForm(initial={
                        'user_id': user.user_id,
                        'user_name': user.user_name,
                        'user_email': user.user_email,
                        'user_phone': user.user_phone_number
                    })
                    # create view
                    return render(request, 'edit_user.html',
                                  {'form': form,
                                   'user_id': user_id,
                                   'deleted': False})
                except KeyError:
                    # value was not in database; return error
                    return HttpResponse("No user with id " + str(user_id))
            else:
                # if method is post
                return submit(request, user_id)
    except KeyError:
        # if no user is logged in
        pass
    # redirect to log in page
    # should only be reached in no user logged in case
    return HttpResponseRedirect("../../login")


def submit(request, user_id):
    """
        Handles the form values passed via POST
    """
    user = User.objects.get(user_id=user_id)
    # grabs the user's information
    # doesn't need try/catch because Django would have returned a 404 at this point if user did not exist
    try:
        if request.POST["user_delete"]:
            # user_delete would only be sent if true
            if user_id == request.session["user_id"]:
                # check if user is trying to delete self while logged in
                # if so, then sends error and redirects to page
                error_message = "Cannot delete currently logged in user"
                form = UserForm(initial={
                    'user_id': user.user_id,
                    'user_name': user.user_email,
                    'user_email': request.POST["user_email"],
                    'user_phone': request.POST["user_phone"]
                })
                return render(request, 'edit_user.html',
                              {'form': form,
                               'user_id': user_id,
                               'deleted': False,
                               'error_message': error_message})
            # if user being deleted is not current account, delete user
            User.objects.get(user_id=user_id).delete()
            # show page stating that delete was successful
            return render(request, 'edit_user.html',
                          {'user_id': user_id,
                           'deleted': True})
    except KeyError:
        # if POST["user_delete"] was not sent (common case)
        pass
    if request.POST["user_email"]:
        try:
            if user_id == request.session["user_id"]:
                # user logged in is being edited, don't change email
                # this prevents annoying cookie manipulation
                error_message = 'Cannot change email address of logged in user.'
                form = UserForm(initial={
                    'user_id': user.user_id,
                    'user_name': user.user_email,
                    'user_email': request.POST["user_email"],
                    'user_phone': request.POST["user_phone"]
                })
                # repopulates form and displays page with an error message
                return render(request, 'edit_user.html',
                              {'form': form,
                               'user_id': user_id,
                               'deleted': False,
                               'error_message': error_message})
            # saves changes to email if no issues caught
            user.user_email = request.POST["user_email"]
            user.save()
        except IntegrityError:
            # error in which email given is not unique
            error_message = 'Account with email address \'' + \
                            str(request.POST["user_email"]) + '\' already exists'
            form = UserForm(initial={
                'user_id': user.user_id,
                'user_name': request.POST["user_name"],
                'user_email': request.POST["user_email"],
                'user_phone': request.POST["user_phone"]
            })
            # repopulates form with values and displays error
            return render(request, 'edit_user.html',
                          {'form': form,
                           'user_id': user_id,
                           'deleted': False,
                           'error_message': error_message})
    if request.POST["user_pass"]:
        # if user attempts to change passwords
        if password_match(request):
            # confirmation email matched regular
            user.user_salt = generate_salt()
            # creates a uniques salt for user
            user.user_password_hash = protected(request, user)
            # then hashes password with salt
            user.save()
            # save changes
        else:
            # case where confirmation password did not match given
            error_message = 'Passwords do not match'
            form = UserForm(initial={
                'user_id': user.user_id,
                'user_name': request.POST["user_name"],
                'user_email': request.POST["user_email"],
                'user_phone': request.POST["user_phone"]
            })
            # repopulates form and redirects back to page with error
            return render(request, 'edit_user.html',
                          {'form': form,
                           'user_id': user_id,
                           'deleted': False,
                           'error_message': error_message})
    if request.POST["user_phone"]:
        # saves changes to phone number
        user.user_phone_number = request.POST["user_phone"]
        user.save()
    if request.POST["user_name"]:
        # saves changes to user name
        user.user_name = request.POST["user_name"]
        user.save()
    form = UserForm(initial={
        'user_id': user.user_id,
        'user_name': request.POST["user_name"],
        'user_email': request.POST["user_email"],
        'user_phone': request.POST["user_phone"]
    })
    # repopulates form and presents a success message
    return render(request, 'edit_user.html',
                  {'form': form,
                   'user_id': user_id,
                   'deleted': False,
                   'success': True})


class UserForm(forms.Form):
    """
         Django form class that creates fields for form in templates/edit_user
    """
    user_name = forms.CharField(label='Name:', max_length=127)
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_phone = forms.CharField(label='VOIP Extension:', max_length=15)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32, required=False)
    user_pass1 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:', max_length=32, required=False)
    user_delete = forms.BooleanField(label="Delete Account?", required=False)
