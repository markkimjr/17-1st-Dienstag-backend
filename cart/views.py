import json
import jwt

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from cart.models    import Cart, Order, OrderStatus, AddressInformation
from user.models    import User
from user.utils     import login_decorator
from product.models import Product
from voucher.models import Voucher

ORDER_STATUS_CHECK = 'checking_out'

class CartView(View):
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

        except (Order.DoesNotExist, Order.MultipleObjectsReturned):
            return JsonResponse({'message': 'INVALID_ORDER'}, status=400)
    
    @login_decorator
    def get(self, request):
        try:
            user_id          = request.user.id
            order            = Order.objects.get(user_id=user_id, order_status__name=ORDER_STATUS_CHECK)
            cart_list        = order.carts.all()
            total_items_list = [{
                'cart_id'      : cart.id,
                'item_id'      : cart.product_id,
                'model_number' : cart.product.model_number,
                'title'        : cart.product.bag_model.name,
                'price'        : cart.product.price,
                'quantity'     : 1,
                'image_url'    : cart.product.image_url
                } for cart in cart_list]
            total_items      = len(total_items_list)

            return JsonResponse({
                'data': {
                    'total_items_list' : total_items_list,
                    'total_items'      : total_items,
                    }}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Order.DoesNotExist:
            return JsonResponse({'message': 'INVALID_ORDER'}, status=400)

    @login_decorator
    def delete(self, request, cart_id): 
        try:
            Cart.objects.get(id=cart_id).delete()
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'INVALID_CART'}, status=400)

class OrderDetailView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
            else:
                user = User.objects.create(email=data['email'], is_anonymous=True)
            
            AddressInformation.objects.create(
                user_id                     = user.id,
                billing_country             = data['billing_country'],
                billing_first_name          = data['billing_first_name'],
                billing_last_name           = data['billing_last_name'],
                billing_street_number       = data['billing_street_number'],
                billing_additional_address  = data['billing_additional_address'],
                billing_district            = data['billing_district'],
                billing_city                = data['billing_city'],
                billing_postal_code         = data['billing_postal_code'],
                billing_phone_number        = data['billing_phone_number'],
                shipping_country            = data['shipping_country'],
                shipping_first_name         = data['shipping_first_name'],
                shipping_last_name          = data['shipping_last_name'],
                shipping_street_number      = data['shipping_street_number'],
                shipping_additional_address = data['shipping_additional_address'],
                shipping_district           = data['shipping_district'],
                shipping_city               = data['shipping_city'],
                shipping_postal_code        = data['shipping_postal_code'],
                shipping_phone_number       = data['shipping_phone_number']
            )
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)