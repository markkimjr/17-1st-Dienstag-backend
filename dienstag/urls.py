from django.urls import path, include

urlpatterns = [
        path('cart', include('cart.urls')),
        path('user', include('user.urls'))
]
