import pathlib
import stripe

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils.text import slugify

from cfehome.env import config

# Obtener la clave secreta de Stripe desde la configuración del entorno
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)

# Establecer la clave secreta de Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Esto es importante para aplicaciones que manejan archivos confidenciales o de propiedad exclusiva
PROTECTED_MEDIA_ROOT = settings.PROTECTED_MEDIA_ROOT
protected_storage = FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    stripe_product_id = models.CharField(max_length=222, blank=True, null=True)
    image = models.ImageField(upload_to="products/",blank=True, null=True)
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True, null=True, max_length=255)
    handle = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price_id = models.CharField(max_length=222, blank=True, null=True)
    # price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    stripe_price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[str(self.handle)])
        
    def get_manage_url(self):
        return reverse("products:product_manage", kwargs={"handle": self.handle})

    def save(self, *args, **kwargs):
        if self.name:
            stripe_product_r = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_r.id
    
        if self.price != self.og_price:
            #price_changed
            self.og_price = self.price
            #trigger and API request for the price
            self.stripe_price = int(self.price * 100)
            if self.stripe_price_id:
                stripe_price_obj = stripe.Price.create(
                    product = self.stripe_product_id,
                    unit_amount= self.stripe_price,
                    currency="usd"
                )
                self.stripe_price_id = stripe_price_obj.id
            self.price_changed_timestamp = timezone.now()
        
        # Si el objeto no tiene un slug o el nombre ha cambiado, crea uno nuevo
            # if not self.handle or self.name != self.handle:
        # Si el objeto no tiene un slug
        if not self.handle:
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

def handle_product_attachment_upload(instance, filename):
    return f"products/{instance.product.handle}/attachments/{filename}"
        
class ProductAttachment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(upload_to=handle_product_attachment_upload,
        storage=protected_storage)
    name = models.CharField(max_length=120, blank=True, null=True)
    is_free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = pathlib.Path(self.file.name).name
            
        super().save(*args, **kwargs)
        
    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name
        
    def get_download_url(self):
        return reverse('products:download', kwargs={"handle": self.product.handle, "pk": self.pk})