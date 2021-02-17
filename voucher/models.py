from django.db import models

class Voucher(models.Model):
    price    = models.DecimalField(max_digits=6, decimal_places=2)
    code     = models.CharField(max_length=100)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'vouchers'


