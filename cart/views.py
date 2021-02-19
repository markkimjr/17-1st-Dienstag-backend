import json
import jwt

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from cart.models    import Cart, Order, OrderStatus, AddressInformation
from user.models    import User
from product.models import Product
from voucher.models import Voucher


class UserCartView(View):
    @login_decorator
    def post(self, request):
        data       = json.loads(request.body)
        user_id    = request.user.id

        Cart.objects.create(
                product_id = 
                user_id    = user_id,
                voucher_id = voucher_id
                )
