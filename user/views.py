import json
import bcrypt
import jwt

from django.http          import JsonResponse
from django.views         import View

from dienstag.my_settings import SECRET, ALGORITHM
from .models              import User, UserInformation
from .utils               import login_decorator
from cart.models          import AddressInformation

class SignUpView(View):
    def post(self, request):
        MINIMUM_PASSWORD_LENGTH = 8
        try:
            data            = json.loads(request.body)
            email           = data['email']
            username        = data['username']
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            phone_number    = data['phone_number']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'ALREADY_EXIST'}, status=400)

            if '@' not in email or '.' not in email:
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=400)
                
            user = User.objects.create(email=email, is_anonymous=False)
            
            UserInformation.objects.create(user=user, username=username, password=hashed_password, phone_number=phone_number)
            
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=401)

            user = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.user_information.get(user=user).password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id}, SECRET, ALGORITHM)
                return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=200)
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class UserView(View):
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
            is_same                     = data['is_same']
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            else:
                user = User.objects.create(email=email, is_anonymous=True)

            if is_same == 'True':
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
                    shipping_country=billing_country,
                    shipping_first_name=billing_first_name,
                    shipping_last_name=billing_last_name,
                    shipping_street_number=billing_street_number,
                    shipping_additional_address=billing_additional_address,
                    shipping_district=billing_district,
                    shipping_city=billing_city,
                    shipping_postal_code=billing_postal_code,
                    shipping_phone_number=billing_phone_number
            )

            if is_same == 'False':
                shipping_country            = data['shipping_country']
                shipping_first_name         = data['shipping_first_name']
                shipping_last_name          = data['shipping_last_name']
                shipping_street_number      = data['shipping_street_number']
                shipping_additional_address = data['shipping_additional_address']
                shipping_district           = data['shipping_district']
                shipping_city               = data['shipping_city']
                shipping_postal_code        = data['shipping_postal_code']
                shipping_phone_number       = data['shipping_phone_number']
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

