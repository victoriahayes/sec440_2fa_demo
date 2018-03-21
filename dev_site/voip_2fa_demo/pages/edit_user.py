from ..models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.db import IntegrityError
from .new_user import password_match, generate_salt, protected


def edit_user(request, user_id):
    try:
        if request.session["user_email"]:
            if request.method == "GET":
                try:
                    user = User.objects.get(user_id=user_id)
                    form = UserForm(initial={
                        'user_id': user.user_id,
                        'user_name': user.user_name,
                        'user_email': user.user_email,
                        'user_phone': user.user_phone_number
                    })
                    return render(request, 'edit_user.html',
                                  {'form': form,
                                   'user_id': user_id,
                                   'deleted': False})
                except KeyError:
                    return HttpResponse("No user with id " + str(user_id))
            else:
                return submit(request, user_id)
    except:
        pass
    return HttpResponseRedirect("../../login")


def submit(request, user_id):
    user = User.objects.get(user_id=user_id)
    try:
        if request.POST["user_delete"]:
            if request.POST["user_delete"]:
                if user_id == request.session["user_id"]:
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
                User.objects.get(user_id=user_id).delete()
                return render(request, 'edit_user.html',
                              {'user_id': user_id,
                               'deleted': True})
    except KeyError:
        pass
    if request.POST["user_email"]:
        try:
            if user_id == request.session["user_id"]:
                error_message = 'Cannot change email address of logged in user.'
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
                               'error_message':error_message})
            user.user_email = request.POST["user_email"]
            user.save()
        except IntegrityError:
            error_message = 'Account with email address \'' + \
                str(request.POST["user_email"]) + '\' already exists'
            form = UserForm(initial={
                'user_id': user.user_id,
                'user_name': request.POST["user_name"],
                'user_email': request.POST["user_email"],
                'user_phone': request.POST["user_phone"]
            })
            return render(request, 'edit_user.html',
                          {'form': form,
                           'user_id': user_id,
                           'deleted': False,
                           'error_message': error_message})
    if request.POST["user_pass"]:
        if password_match(request):
            user.user_salt = generate_salt()
            user.user_password_hash = protected(request, user)
            user.save()
        else:
            error_message = 'Passwords do not match'
            form = UserForm(initial={
                'user_id': user.user_id,
                'user_name': request.POST["user_name"],
                'user_email': request.POST["user_email"],
                'user_phone': request.POST["user_phone"]
            })
            return render(request, 'edit_user.html',
                          {'form': form,
                           'user_id': user_id,
                           'deleted': False,
                           'error_message': error_message})
    if request.POST["user_phone"]:
        user.user_phone_number = request.POST["user_phone"]
        user.save()
    if request.POST["user_name"]:
        user.user_name = request.POST["user_name"]
        user.save()
    form = UserForm(initial={
        'user_id': user.user_id,
        'user_name': request.POST["user_name"],
        'user_email': request.POST["user_email"],
        'user_phone': request.POST["user_phone"]
    })
    return render(request, 'edit_user.html',
                  {'form': form,
                   'user_id': user_id,
                   'deleted': False,
                   'success': True})


class UserForm(forms.Form):
    user_name = forms.CharField(label='Name:', max_length=127)
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_phone = forms.CharField(label='VOIP Extension:', max_length=15)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32, required=False)
    user_pass1 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:', max_length=32, required=False)
    user_delete = forms.BooleanField(label="Delete Account?", required=False)
