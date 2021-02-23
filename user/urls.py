from django.urls import path

from user.views  import SignUpView, SignInView, NonMemberView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/checkout', NonMemberView.as_view()),
]