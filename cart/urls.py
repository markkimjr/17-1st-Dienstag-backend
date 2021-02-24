from django.urls import path

from cart.views  import CartView, CartProductView, CartVoucherView

urlpatterns = [
        path('', CartView.as_view()),
        path('/<int:cart_id>', CartView.as_view()),
        path('/product', CartProductView.as_view()),
        path('/voucher', CartVoucherView.as_view()),
        ]
