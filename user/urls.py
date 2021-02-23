from django.urls import path

from user.views  import SignUpView, SignInView, UserView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/checkout', UserView.as_view()),
]