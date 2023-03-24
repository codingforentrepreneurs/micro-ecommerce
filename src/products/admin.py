from django.contrib import admin

# Register your models here.
from .models import Product, ProductAttachment

admin.site.register(Product)


admin.site.register(ProductAttachment)