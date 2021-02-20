from django.urls import path

from cart.views  import UserCartView

urlpatterns = [
        path('/user', UserCartView.as_view())
        ]
