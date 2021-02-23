import json
import jwt

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from cart.models    import Cart, Order, OrderStatus, AddressInformation
from user.models    import User
from product.models import Product
from voucher.models import Voucher

class OrderDetailView(View):
    def post(self, request):
        try:
            data                        = json.loads(request.body)
            email                       = data['email']
            billing_country             = data['billing_country']
            billing_first_name          = data['billing_first_name']
            billing_last_name           = data['billing_last_name']
            billing_street_number       = data['billing_street_number']
            billing_additional_address  = data['billing_additional_address']
            billing_district            = data['billing_district']
            billing_city                = data['billing_city']
            billing_postal_code         = data['billing_postal_code']
            billing_phone_number        = data['billing_phone_number']
            shipping_country            = data['shipping_country']
            shipping_first_name         = data['shipping_first_name']
            shipping_last_name          = data['shipping_last_name']
            shipping_street_number      = data['shipping_street_number']
            shipping_additional_address = data['shipping_additional_address']
            shipping_district           = data['shipping_district']
            shipping_city               = data['shipping_city']
            shipping_postal_code        = data['shipping_postal_code']
            shipping_phone_number       = data['shipping_phone_number']
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            else:
                user = User.objects.create(email=email, is_anonymous=True)
            
            AddressInformation.objects.create(
                user_id=user.id,
                billing_country=billing_country,
                billing_first_name=billing_first_name,
                billing_last_name=billing_last_name,
                billing_street_number=billing_street_number,
                billing_additional_address=billing_additional_address,
                billing_district=billing_district,
                billing_city=billing_city,
                billing_postal_code=billing_postal_code,
                billing_phone_number=billing_phone_number,
                shipping_country=shipping_country,
                shipping_first_name=shipping_first_name,
                shipping_last_name=shipping_last_name,
                shipping_street_number=shipping_street_number,
                shipping_additional_address=shipping_additional_address,
                shipping_district=shipping_district,
                shipping_city=shipping_city,
                shipping_postal_code=shipping_postal_code,
                shipping_phone_number=shipping_phone_number
            )
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
