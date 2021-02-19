import json
import jwt

from django.views    import View
from django.http     import JsonResponse, HttpResponse

from cart.models     import Cart
from user.models     import User
from products.models import Product
from voucher.models  import Voucher


class CartView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_id = data['user_id']
        

        Cart.objects.create(
                product_id = 
                user_id    = user_id,
                voucher_id = voucher_id
                )
