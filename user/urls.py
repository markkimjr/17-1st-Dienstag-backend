from django.urls import path

from user.views  import SignUpView, SignInView, LogoutView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/logout', LogoutView.as_view()),
]