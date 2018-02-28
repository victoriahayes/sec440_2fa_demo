from ..models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect


def all_users(request):
    try:
        request.session["user_name"]
    except KeyError:
        return HttpResponseRedirect("login")

    users = User.objects.values("user_id", "user_email", "user_name")
    print(users)
    return render(request, "users.html",
                  {
                      'all_users': users
                  })
