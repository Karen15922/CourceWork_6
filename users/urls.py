from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (NewPasswordView, ProfileView, RegisterView,
                         UserListView, UserUpdateView, email_verification)

app_name = UsersConfig.name

# урлы приложения users
urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("reset-pasword/", NewPasswordView.as_view(), name="reset-password"),
    path("users_list/", UserListView.as_view(), name="users_list"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="user_update"),
]
