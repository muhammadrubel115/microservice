from django.urls import path
<<<<<<< HEAD
from authentication.views import RegisterView, LoginView
=======
from authentication.views import RegisterView, LoginView, MeView, PermissionsView
>>>>>>> 973a508fb6725d5c50031b2761615495605f5045


# brainless/auth/urls.py
urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
<<<<<<< HEAD
   
   
=======
    path("me/", MeView.as_view(), name="auth-me"),
    path("permissions/", PermissionsView.as_view(), name="auth-permissions"),
>>>>>>> 973a508fb6725d5c50031b2761615495605f5045
]
