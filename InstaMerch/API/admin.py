from django.contrib import admin
from .models import Designer, Address, Design, Orders

# Register your models here.

admin.site.register(Designer)
admin.site.register(Address)
admin.site.register(Design)
admin.site.register(Orders)
