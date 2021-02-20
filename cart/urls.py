from django.urls import path

from cart.views  import UserCartView, UserCartDetailView

urlpatterns = [
        path('', UserCartView.as_view()),
        path('/items', UserCartDetailView.as_view()),
        path('/items/<int:product_id>')
        ]
