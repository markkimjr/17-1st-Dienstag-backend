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
                return JsonResponse({'message': 'SUCCESS', 'access_token': token, 'email': email, 'username': user.user_information.get(user=user).username}, status=200)
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)