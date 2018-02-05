from django.urls import path
from .pages import index, login, new_user

urlpatterns = [
    path('', index.index, name='index'),
    path('user/new', new_user.new_user_form, name='user/new'),
    path('login', login.login, name='login')
]
