from django.urls import path

from cart.views  import CartView, NonUserCartView

urlpatterns = [
        path('', CartView.as_view()),
        path('/<int:cart_id>', CartView.as_view()),
        path('/nonuser', NonUserCartView.as_view()),
        path('/nonuser/<int:product_id>', NonUserCartView.as_view())
        ]

