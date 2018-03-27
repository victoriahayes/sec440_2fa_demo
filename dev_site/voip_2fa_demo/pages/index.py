from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import User

base_path = 'dev_site/'

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
            return HttpResponseRedirect("login")
        return 
    except KeyError:
        if no_users():
              return HttpResponseRedirect("user/add")
        return HttpResponseRedirect(base_path  + "login")

def no_users():
    user_count = User.objects.all().count()
    if user_count == 0:
        return True
    return False
