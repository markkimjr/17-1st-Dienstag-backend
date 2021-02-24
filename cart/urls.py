from django.urls import path

from cart.views  import OrderDetailView

urlpatterns = [
    path('/checkout', OrderDetailView.as_view()),
]