from django.contrib import admin
from .models import Account, Address, Design, Order, Category

admin.site.register(Account)
admin.site.register(Address)
admin.site.register(Design)
admin.site.register(Order)
admin.site.register(Category)
