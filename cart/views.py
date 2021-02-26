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

class NonUserCartView(View):
    def get(self, request, product_id):
        try:
            product      = Product.objects.get(id=product_id)
            product_info = [{
                'item_id'      : product_id,
                'model_number' : product.model_number,
                'title'        : product.bag_model.name,
                'price'        : product.price,
                'quantity'     : 1,
                'image_url'    : product.images.all()[0].image_url
                }]
            
            return JsonResponse({'data': product_info}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({'message': 'INVALID_PRODUCT'}, status=400)

    def post(self, request):
        try:
            data                        = json.loads(request.body)
            product_list                = data['product_list']
            email                       = data['email']
            shipping_first_name         = data['shipping_first_name']
            shipping_last_name          = data['shipping_last_name']
            shipping_district           = data['shipping_district']
            shipping_city               = data['shipping_city']
            shipping_postal_code        = data['shipping_postal_code']
            shipping_phone_number       = data['shipping_phone_number']
            shipping_street_number      = data['shipping_street_number']
            shipping_product_list       = data['shipping_product_list']
            shipping_additional_address = data.get('shipping_additional_address')
            billing_first_name          = data['billing_first_name']
            billing_last_name           = data['billing_last_name']
            billing_district            = data['billing_district']
            billing_city                = data['billing_city']
            billing_postal_code         = data['billing_postal_code']
            billing_phone_number        = data['billing_phone_number']
            billing_street_number       = data['billing_street_number']
            billing_product_list        = data['billing_product_list']
            billing_additional_address  = data.get('billing_additional_address')

            user = User.objects.create(
                    email        = email,
                    is_anonymous = True
                    )
            
            address = AddressInformation.objects.create(
                    shipping_first_name         = shipping_first_name,
                    shipping_last_name          = shipping_first_name,
                    shipping_district           = shipping_district,
                    shipping_city               = shipping_city,
                    shipping_postal_code        = shipping_postal_code,
                    shipping_phone_number       = shipping_phone_number,
                    shipping_street_number      = shipping_street_number,
                    shipping_additional_address = shipping_additional_address,
                    billing_first_name          = billing_first_name,
                    billing_last_name           = billing_first_name,
                    billing_district            = billing_district,
                    billing_city                = billing_city,
                    billing_postal_code         = billing_postal_code,
                    billing_phone_number        = billing_phone_number,
                    billing_street_number       = billing_street_number,
                    billing_additional_address  = billing_additional_address
                    )

            order = Order.objects.create(
                    user_id                = user.id,
                    order_status_id        = OrderStatus.objects.get(name=ORDER_STATUS_CHECK).id,
                    address_information_id = address.id
                    )

            for i in range(product_list):
                Cart.objects.create(
                product_id = product_list[i],
                order_id = order.id 
                )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
