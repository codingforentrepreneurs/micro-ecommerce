from django.contrib import admin
from .models import Product,ProductAttachment
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductAttachment)
# admin.site.register(CustomUser)