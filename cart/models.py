from django.db import models

from product.models import Product
from voucher.models import Voucher
from user.models    import User


class Cart(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='carts')
    voucher = models.ForeignKey('voucher.Voucher', on_delete=models.CASCADE, related_name='carts')

    class Meta:
        db_table = 'carts'

class Order(models.Model):
    billing_country             = models.CharField(max_length=100)
    billing_first_name          = models.CharField(max_length=100)
    billing_last_name           = models.CharField(max_length=100)
    billing_street_number       = models.CharField(max_length=100)
    billing_additional_address  = models.CharField(max_length=100, null=True)
    billing_district            = models.CharField(max_length=100)
    billing_city                = models.CharField(max_length=100)
    billing_postal_code         = models.CharField(max_length=100)
    billing_phone_number        = models.CharField(max_length=100)
    shipping_country            = models.CharField(max_length=100)
    shipping_first_name         = models.CharField(max_length=100)
    shipping_last_name          = models.CharField(max_length=100)
    shipping_street_number      = models.CharField(max_length=100)
    shipping_additional_address = models.CharField(max_length=100, null=True)
    shipping_district           = models.CharField(max_length=100)
    shipping_city               = models.CharField(max_length=100)
    shipping_postal_code        = models.CharField(max_length=100)
    shipping_phone_number       = models.CharField(max_length=100)
    user                        = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, related_name='orders')
    cart                        = models.ForeignKey('Cart', on_delete=models.SET_NULL, null=True, related_name='orders')

    class Meta:
        db_table = 'orders'


