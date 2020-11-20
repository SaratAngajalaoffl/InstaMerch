from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(
        upload_to='images/profile_pics', blank=True, null=True,default="images/profile_pics/avatar.png")

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username


class Address(models.Model):
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    account = models.ForeignKey('Account', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.address_line1


class Category(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Design(models.Model):
    title = models.CharField(max_length=10)
    picture = models.ImageField(upload_to='images/designs')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    isfeatured = models.BooleanField(default=False)
    createdon = models.DateField(auto_now_add=True)
    purchases = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class Order(models.Model):
    products = models.ManyToManyField('Design')
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    session_id = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=50, default='Awaiting Payment Confirmation')
    placed_on = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(
        'Account', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        if self.account:
            return str(self.account)
        else:
            s = ""
            for product in self.products.all():
                s = s + str(product) + ","  
            return s[:-1]