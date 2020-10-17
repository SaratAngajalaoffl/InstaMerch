from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Designer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)

    def __str__(self):
        return self.address_line1


class Design(models.Model):
    picture = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=10)
    price = models.IntegerField()
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)

    def __str__(self):
        return self.category


class Order(models.Model):
    product = models.OneToOneField(Design, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, null=True, blank=True)
    delivery_address = models.OneToOneField(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Order Recieved')
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.category
