from django.urls import path

from cart.views  import CartView, CartProductView

urlpatterns = [
        path('', CartView.as_view()),
        path('/<int:cart_id>', CartView.as_view()),
        path('/product', CartProductView.as_view()),
        ]

