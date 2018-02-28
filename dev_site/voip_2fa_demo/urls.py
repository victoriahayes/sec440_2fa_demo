from django.urls import path
from .pages import index, login, new_user, users, edit_user

urlpatterns = [
    path('', index.index, name='index'),
    path('user/new', new_user.new_user_form, name='user/new'),
    path('login', login.login, name='login'),
    path('users', users.all_users, name="users"),
    path('user/edit/<int:user_id>', edit_user.edit_user, name="edit_user")
]
