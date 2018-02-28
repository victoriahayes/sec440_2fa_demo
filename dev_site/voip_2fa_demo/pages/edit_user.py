from ..models import User
from django.shortcuts import render
from django.http import HttpResponse
from django import forms


def edit_user(request, user_id):
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


def submit(request, user_id):
    print(user_id)
    user = User.objects.get(user_id=user_id)
    #if request.POST["user_email"]:
    return HttpResponse("your mom")
    """new_user.user_name = request.POST['user_name']
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
"""

class UserForm(forms.Form):
    user_name = forms.CharField(label='Name:', max_length=127)
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_phone = forms.CharField(label='VOIP Extension:', max_length=15)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32, required=False)
    user_pass1 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password:', max_length=32, required=False)
    user_delete = forms.BooleanField(label="Delete Account?", required=False)
