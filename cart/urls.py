from django.urls import path

from cart.views  import UserCartView, UserCartProductView, UserCartVoucherView, UserCartDetailView

urlpatterns = [
        path('', UserCartView.as_view()),
        path('/<int:item_id>', UserCartDetailView.as_view()),
        path('/product', UserCartProductView.as_view()),
        path('/voucher', UserCartVoucherView.as_view()),
        ]
