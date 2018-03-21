from django.http import HttpResponseRedirect
from django.shortcuts import render

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
            return HttpResponseRedirect("./login")
        return 
    except KeyError:
        return HttpResponseRedirect("./login")
