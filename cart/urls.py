from django.urls import path

from cart.views  import UserCartView, UserCartDetailView

urlpatterns = [
        path('', UserCartView.as_view()),
        path('/<int:item_id>', UserCartDetailView.as_view()),
        ]
