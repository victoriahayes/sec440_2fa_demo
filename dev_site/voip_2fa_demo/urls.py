from django.urls import path
from .pages import index, login, new_user

urlpatterns = [
    path('', index.index, name='index'),
    path('user/new', new_user.NewUserForm, name='user/new'),
    path('user/submit', new_user.submit, name='user/submit'),
    path('login', login.login, name='login')
]
