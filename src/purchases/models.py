from django.db import models
from django.conf import settings

from products.models import Product

# Create your models here.
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    stripe_checkout_session_id = models.CharField(max_length=222, null=True, blank=True)
    stripe_price = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)