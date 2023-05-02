from django.utils import timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    # stripe_product_id =
    image = models.ImageField(upload_to="products/",blank=True, null=True)
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True, null=True, max_length=255)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    # stripe_price_id = models.DecimalField()
    # price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[str(self.handle)])

    def save(self, *args, **kwargs):
        if self.price != self.og_price:
            #price_changed
            self.og_price = self.price
            #trigger and API request for the price
            self.stripe_price = int(self.price * 100)
            self.price_changed_timestamp = timezone.now()
        
        # Si el objeto no tiene un slug o el nombre ha cambiado, crea uno nuevo
        if not self.handle or self.name != self.handle:
            self.handle = slugify(self.name)
        # Verifica si el slug ya existe en la base de datos
        if Product.objects.filter(handle=self.handle).exists():
            # El sufijo se establece en el número de objetos Product existentes que ya tienen el mismo slug base.
            max_num = Product.objects.filter(handle__startswith=self.handle).count()
            # Se agrega un sufijo numérico al slug para hacerlo único
            self.handle = f"{self.handle}-{max_num+1}"
                
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.handle