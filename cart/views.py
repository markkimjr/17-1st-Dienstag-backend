import json
import jwt

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from cart.models    import Cart, Order, OrderStatus, AddressInformation
from user.models    import User
from user.utils     import login_decorator
from product.models import Product
from voucher.models import Voucher
from user.utils     import login_decorator

ORDER_STATUS_CHECK = 'checking_out'

class CartProductView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data.get('product_id')
            user_id    = request.user.id

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message': 'INVALID_PRODUCT'}, status=400)

            if Order.objects.filter(user_id=user_id, order_status__name=ORDER_STATUS_CHECK, carts__product_id=product_id).exists():
                return JsonResponse({'message': False}, status=403)

            if Order.objects.filter(user_id=user_id, order_status__name=ORDER_STATUS_CHECK).exists():
                Cart.objects.create(
                    product_id = product_id, 
                    order_id   = Order.objects.get(user_id=user_id, order_status__name=ORDER_STATUS_CHECK).id
                    )
                return JsonResponse({'message': 'SUCCESS'}, status=201)

            order = Order.objects.create(
                    user_id         = user_id,
                    order_status_id = OrderStatus.objects.get(name=ORDER_STATUS_CHECK).id
                    )

            Cart.objects.create(
                    product_id = product_id,
                    order_id   = order.id
                    )

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class CartVoucherView(View):
    @login_decorator
    def post(self, request):
        try:
            data             = json.loads(request.body)
            voucher_quantity = data.get('voucher_quantity')
            voucher_price    = data.get('voucher_price')
            voucher_code     = data.get('voucher_code')
            user_id          = request.user.id

            if Order.objects.filter(user_id=user_id, order_status__name=ORDER_STATUS_CHECK).exists():
                Cart.objects.create(
                        voucher_id = Voucher.objects.create(
                            price    = voucher_price,
                            code     = voucher_code,
                            quantity = voucher_quantity).id,
                        order_id   = Order.objects.get(user_id=user_id, order_status__name=ORDER_STATUS_CHECK).id
                        )
                return JsonResponse({'message': 'SUCCESS'}, status=201) 

            order = Order.objects.create(
                    user_id         = user_id,
                    order_status_id = OrderStatus.objects.get(name=ORDER_STATUS_CHECK
                    ).id
                    )

            Cart.objects.create(
                    voucher_id = Voucher.objects.create(
                        price    = voucher_price,
                        code     = voucher_code,
                        quantity = voucher_quantity).id,
                    order_id   = order.id
                    )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class CartView(View):
    @login_decorator
    def get(self, request):
        try:
            user_id          = request.user.id
            order            = Order.objects.get(user_id=user_id, order_status__name=ORDER_STATUS_CHECK)
            cart_list        = order.carts.all()
            total_items_list = [{
                'cart_id'      : cart.id,
                'item_id'      : cart.product_id if not cart.voucher else cart.voucher_id,
                'model_number' : cart.product.model_number if not cart.voucher else cart.voucher.code,
                'title'        : cart.product.bag_model.name if not cart.voucher else None,
                'price'        : cart.product.price if not cart.voucher else cart.voucher.price,
                'quantity'     : 1 if not cart.voucher else cart.voucher.quantity,
                'image_url'    : cart.product.images.all()[0].image_url if not cart.voucher else None
                } for cart in cart_list]
            total_items      = len(total_items_list)

            return JsonResponse({
                'data': {
                    'total_items_list' : total_items_list,
                    'total_items'      : total_items
                    }}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, cart_id): 
        try:
            Cart.objects.get(id=cart_id).delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'INVALID_CART'}, status=400)
