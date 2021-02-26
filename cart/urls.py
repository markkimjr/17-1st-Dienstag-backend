from django.urls import path

from cart.views  import OrderDetailView

urlpatterns = [
    path('', CartView.as_view()),
    path('/<int:cart_id>', CartView.as_view()),
    path('/checkout', OrderDetailView.as_view()),
]