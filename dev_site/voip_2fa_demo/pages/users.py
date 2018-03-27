from ..models import User
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect


def all_users(request):
    """
        Django page handler for /users
    """
    try:
        request.session["user_name"]
        # check if logged in
    except KeyError:
        # not logged in
        return HttpResponseRedirect(reverse("login"))
        # redirect to login page
    users = User.objects.values("user_id", "user_email", "user_name")
    # grabs all users from database
    return render(request, "users.html",
                  {
                      'all_users': users
                  })
    # displays list of users in browser
