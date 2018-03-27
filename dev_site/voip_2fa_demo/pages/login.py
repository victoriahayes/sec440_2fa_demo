from django import forms
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import exceptions
from .new_user import protected
from .callFormatter import generateCallFile
import random
import smtplib
from .index import no_users
from email.mime.text import MIMEText

from ..models import User


def submit(request):
    """
        handles information passed in log in form
    """
    try:
        request.session['attempts'] += 1
        user_data = User.objects.get(user_email=request.session['user_email'])
        # grabs user information for given email
        correct_code = user_data.user_2FA_code
        if request.POST['user_2fa_code'] == correct_code:
            # if given 2FA code is correct
            request.session['login_complete'] = True
            del request.session['attempts']
            user_data.user_2FA_code = ""
            user_data.save()
            # removes current 2FA code
            return HttpResponseRedirect(reverse('index'))
            # redirects to index
        else:
            if request.session['attempts'] == 3:
                # if on 3rd attempt and code still incorrect
                notify_admin(request)
                # send message to /var/mail
                del request.session['attempts']
                del request.session['user_name']
                del request.session['user_email']
                del request.session['login_complete']
                # clear cookies
                user_data.user_2FA_code = ""
                user_data.save()
                # remove 2FA code
                return render(request, 'login.html', {
                    'form': LoginForm,
                    'error_message': "Two-factor authentication failed for user."
                })
                # display error message on login page
            else:
                # code incorrect, but less than 3 strikes
                attempts_remaining = 3 - request.session['attempts']
                send_2fa_code(user_data)
                # call user
                return render(request, "login.html", {
                    'form': TwoFaForm,
                    'error_message': "Code incorrect. Attempts remaining: " + str(attempts_remaining)
                })
                # displays form requesting 2fa code with error messsage
    except KeyError:
        # if no previous attempts to enter 2FA code
        user_data = find_user(request)
        # grab user information
        if type(user_data) == HttpResponse:
            # if failed to grab user information
            return user_data
        password_check_response = check_password(user_data, request)
        # sees if password matches that of user
        if password_check_response is not None:
            return password_check_response
            # returns error message on page
        # if password correct
        request.session['user_name'] = user_data.user_name
        request.session['user_email'] = user_data.user_email
        request.session["user_id"] = user_data.user_id
        request.session['login_complete'] = False
        request.session['attempts'] = 0
        # sets cookies
        generate_2fa_code(user_data)
        # creates 6-digit code
        send_2fa_code(user_data)
        # calls users
        return render(request, "login.html", {
            "form": TwoFaForm,
            "error_message": None
        })
        # display form for entering 2FA code


def find_user(request):
    """
        attempts to pull user's information from the form's email address
    """
    try:
        user_data = User.objects.get(
            user_email=request.POST['user_email']
        )
        return user_data
        # returns user information
    except exceptions.ObjectDoesNotExist:
        # user data not found
        return render(request, "login.html", {
            "error_message": str("No user with email " +
                                 str(request.POST['user_email']) +
                                 " exists"),
            "form": LoginForm(initial={
                "user_email": request.POST['user_email']
            })
        })
        # redirect to login form with error message


def check_password(user_data, request):
    """
        hashes the password given in the form
        then compares it to user's hashed password
    """
    hashed_pw = protected(request, user_data)
    # hashes password
    if hashed_pw != user_data.user_password_hash:
        # if passwords don't match
        return render(request, "login.html", {
            "error_message": "Password for user " +
                             str(request.POST['user_email']) +
                             " is incorrect",
            "form": LoginForm(initial={
                "user_email": request.POST['user_email']
            })
        })
        # redirects back to form with error message
    else:
        # passwords matched
        return None


def get_client_ip(request):
    """
         grabs the ip address of request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        # request has multiple ips listed, only grab first
    else:
        ip = request.META.get('REMOTE_ADDR')
        # request had one ip listed
    return ip


def notify_admin(request):
    """
        sends message to root about multiple failed login attempts
    """
    client_ip = get_client_ip(request)
    # grabbed ip

    message = str.format("3 Failed login attempts to user account {0} from ip address {1}",
                         str(request.session['user_email']), client_ip)
    msg = MIMEText(message)
    # formatted message
    msg['Subject'] = '2FA security alert'
    msg['From'] = 'asterisk'
    msg['To'] = 'root'
    # formatted message to have to/from/subject
    s = smtplib.SMTP('localhost')
    # use localhost's smtp server
    s.sendmail('victoria', 'root', msg.as_string())
    # send message
    s.quit()
    # close connection to smtp server


def generate_2fa_code(user_data):
    """
        generates cryptographically secure 6-digit code
        will break if running on python 3.6
    """
    code = ""
    for i in range(6):
        code += str(random.SystemRandom().randint(0, 9))
        # concatenated randomly generated int to code
    user_data.user_2FA_code = code
    user_data.save()
    # saves the code to database


def send_2fa_code(user):
    """
        creates call file that triggers phone call
    """
    user_phone = user.user_phone_number
    user_2fa = user.user_2FA_code
    # grab user information
    generateCallFile(str(user_2fa), user_phone)
    # generated call


class LoginForm(forms.Form):
    """
        Django form for username/password to display in templates/login
    """
    user_email = forms.EmailField(label='Email:', max_length=127)
    user_pass = forms.CharField(widget=forms.PasswordInput(), label='Password:', max_length=32)


class TwoFaForm(forms.Form):
    """
        Django form for 2FA code to display in templates/login
    """
    user_2fa_code = forms.CharField(label='Validation code:', max_length=8)


def login(request):
    """
         Django page handler for login
    """
    if no_users():
        # without users in database, it is impossible to log in
        return HttpResponseRedirect(reverse("user/new"))
        # redirects to user creation page
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'login.html',
                      {'form': login_form,
                       'error_message': None
                       })
        # displays empty log in form
    else:
        # if request.method == post
        return submit(request)
        # handles form data
