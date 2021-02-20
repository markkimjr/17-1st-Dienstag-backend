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
        try:
            data       = json.loads(request.body)
            product_id = data.get('product_id')
            voucher_id = data.get('voucher_id')
            user_id    = request.user.id

            if product_id:
                if OrderStatus.objects.get(name='checking_out').orders.filter(user_id=user_id).exists():
                    Cart.objects.create(
                        product_id = product_id, 
                        user_id    = user_id,
                        order_id   = Order.objects.get(user_id=user_id, order_status=1).id
                        )

                    return JsonResponse({'message': 'SUCCESS'}, status=201)

                else:
                    Order.objects.create(
                            user_id      = user_id,
                            order_status = 1
                            )

                    Cart.objects.create(
                            user_id    = user_id,
                            product_id = product_id,
                            order_id   = Order.objects.get(user_id=user_id, order_status=1).id
                            )

                    return JsonResponse({'message': 'SUCCESS'}, status=201)

            if voucher_id:
                if OrderStatus.objects.get(name="checking_out").orders.filter(user_id=user_id).exists():
                    Cart.objects.create(
                            voucher_id = voucher_id,
                            user_id    = user_id,
                            order_id   = Order.objects.get(user_id=user_id, order_status=1).id
                            )

                    return JsonResponse({'message': 'SUCCESS'}, status=201)

                else:
                    Order.objects.create(
                            user_id      = user_id,
                            order_status = 1
                            )

                    Cart.objects.create(
                            user_id    = user_id,
                            product_id = product_id,
                            order_id   = Order.objects.get(user_id=user_id, order_status=1).id
                            )

                    return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
