from django.urls import path

from user.views  import OrderDetailView

urlpatterns = [
    path('/checkout', OrderDetailView.as_view()),
]