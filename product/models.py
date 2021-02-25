from django.db import models

class BagType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'bag_types'

class BagModel(models.Model):
    name     = models.CharField(max_length=100)
    bag_type = models.ForeignKey('BagType', on_delete=models.CASCADE, related_name='bag_models')

    class Meta:
        db_table = 'bag_models'

class Product(models.Model):
    model_number = models.CharField(max_length=100)
    price        = models.DecimalField(max_digits=15, decimal_places=2)
    description  = models.TextField()
    bag_model    = models.ForeignKey('BagModel', on_delete=models.CASCADE, related_name='products')
    color        = models.ForeignKey('Color', on_delete=models.CASCADE, related_name='products')
    size         = models.ForeignKey('Size', on_delete=models.CASCADE, related_name='products')
    image_url    = models.URLField(max_length=2000)

    class Meta:
        db_table = 'products'

class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'colors'

class Size(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'sizes'

class Recommendation(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='recommendations')
    bag_model = models.ForeignKey('BagModel', on_delete=models.CASCADE, related_name='recommendations')

    class Meta:
        db_table = 'recommendations'
