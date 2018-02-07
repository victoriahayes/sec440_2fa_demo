from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    try:
        return HttpResponse("Hello, " + str(request.session["user_name"]))
    except KeyError:
        return HttpResponseRedirect("login")
