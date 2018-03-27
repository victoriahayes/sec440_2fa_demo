from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from ..models import User

def index(request):
    """
         Django page handler for home
    """
    try:
        user_name = request.session["user_name"]
        # if logged in
        if request.method == "GET":
            # display templates/index with user_name filled out
            return render(request, 'index.html',
                          {'user_name': user_name})
        else:
            # if post and logged in
            try:
                # deletes all the session cookies to log out user
                del request.session['user_name']
                del request.session['user_email']
                del request.session['user_id']
                del request.session['login_complete']
            except KeyError:
                # for some reason, one of the session cookies were not set
                pass
            return HttpResponseRedirect(reverse("login"))
            # redirects to login page
    except KeyError:
        # if no user logged in
        if no_users():
            # it is impossible to log in if there's no user accounts
            # redirects to user adding page
            return HttpResponseRedirect(reverse("user/add"))
        return HttpResponseRedirect(reverse("login"))
        # redirects to login page


def no_users():
    """
        returns true if there are no entries in user table
    """
    user_count = User.objects.all().count()
    if user_count == 0:
        return True
    return False
