from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=200, unique=True)
    is_anonymous = models.BooleanField()

    class Meta:
        db_table = 'users'

class UserInformation(models.Model):
    password     = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=100)
    username     = models.CharField(max_length=100, unique=True)
    user         = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_information')

    class Meta:
        db_table = 'user_information'
