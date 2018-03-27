from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from ..models import User


def index(request):
    try:
        user_name = request.session["user_name"]
        if request.method == "GET":
            return render(request, 'index.html',
                          {'user_name': user_name})
        else:
            try:
                 del request.session['user_name']
                 del request.session['user_email']
                 del request.session['user_id']
                 del request.session['login_complete']
            except KeyError:
                 pass
            return HttpResponseRedirect(reverse("login"))
        return 
    except KeyError:
        if no_users():
              return HttpResponseRedirect(reverse("user/add"))
        return HttpResponseRedirect(reverse("login"))

def no_users():
    user_count = User.objects.all().count()
    if user_count == 0:
        return True
    return False
