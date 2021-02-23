from django.urls import path

from cart.views  import CartView, CartProductView, CartVoucherView, CartDetailView

urlpatterns = [
        path('', CartView.as_view()),
        path('/<int:item_id>', CartDetailView.as_view()),
        path('/product', CartProductView.as_view()),
        path('/voucher', CartVoucherView.as_view()),
        ]
