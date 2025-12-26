from django.urls import path
from authentication.views import RegisterView, LoginView


# brainless/auth/urls.py
urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
   
   
]
