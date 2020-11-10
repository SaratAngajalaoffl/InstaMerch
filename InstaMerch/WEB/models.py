from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.

class Cart(models.Model):
    item = models.ManyToManyField("API.Design", null=True, blank=True)
    account = models.OneToOneField("API.Account",on_delete=CASCADE)

    def __str__(self):
        return str(self.account) + "'s Cart"