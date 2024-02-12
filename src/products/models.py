from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import pathlib
import stripe
from django.urls import reverse
# from django.contrib.auth.models import AbstractUser



from cfehome.env import config

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY",default=None)
stripe.api_key=STRIPE_SECRET_KEY

PROTECTED_MEDIA_ROOT=settings.PROTECTED_MEDIA_ROOT
protected_storage=FileSystemStorage(location=str(PROTECTED_MEDIA_ROOT))
# Create your models here.
class Product(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    name=models.CharField(max_length=120)
    handle=models.SlugField(unique=True)
    image=models.ImageField(upload_to='products/',blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
    og_price=models.DecimalField(max_digits=10,decimal_places=2,default=9.99)
    stripe_product_id=models.CharField(max_length=220,blank=True,null=True)
    stripe_price_id=models.CharField(max_length=320,blank=True,null=True)
    sp_id=models.CharField(max_length=320,blank=True,null=True)
    stripe_price=models.IntegerField(default=999)#100*price
    price_changed_timestramp=models.DateTimeField(auto_now=False,auto_now_add=False,blank=True,null=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def save(self,*args,**kwargs):
        if self.name:
            stripe_product_r=stripe.Product.create(name=self.name)
            self.stripe_product_id=stripe_product_r.id
            stripe_price_obj=stripe.Price.create(product=self.stripe_product_id
                                         ,unit_amount=self.stripe_price,
                                         currency="usd"
                                         )
            self.stripe_price_id=stripe_price_obj.id
            # self.stripe_price_id=stripe.Price.retrieve(id=stripe_price_obj.id).id
        if not self.stripe_price_id:
            stripe_product_r=stripe.Product.create(name=self.name)
            self.stripe_product_id=stripe_product_r.id
            stripe_price_obj=stripe.Price.create(product=self.stripe_product_id
                                         ,unit_amount=self.stripe_price,
                                         currency="usd"
                                         )
            # self.stripe_price_id=stripe.Price.retrieve(id=stripe_price_obj.id).id
            self.stripe_price_id=stripe_price_obj.id
        if self.price!=self.og_price:
        #price changed
            self.og_price=self.price
            self.stripe_price=int(self.price*100)
            #trigger an API request
            if self.stripe_product_id:
                    stripe_price_obj=stripe.Price.create(product=self.stripe_product_id
                                         ,unit_amount=self.stripe_price,
                                         currency="usd"
                                         )
                    self.stripe_price_id=stripe_price_obj.id
        self.price_changed_timestramp=timezone.now()
        super().save(*args,**kwargs)



    # def get_stripe_id(self):
            # if not self.sp_id:
            #     stripe_product_r=stripe.Product.create(name=self.name)
            #     self.stripe_product_id=stripe_product_r.id
            #     stripe_price_obj=stripe.Price.create(product=self.stripe_product_id
            #                              ,unit_amount=self.stripe_price,
            #                              currency="usd"
            #                              )
            #     self.sp_id=stripe.Price.retrieve(id=stripe_price_obj.id).id

            # # stripe_product_r=stripe.Product.create(name=self.name)
            # # self.stripe_product_id=stripe_product_r.id
            # # stripe_price_obj=stripe.Price.create(product=self.stripe_product_id
            # #                              ,unit_amount=self.stripe_price,
            # #                              currency="usd"
            # #                              )
            # # self.sp_id=stripe.Price.retrieve(id=stripe_price_obj.id).id
            # super().save()
            

    @property
    def display_name(self):
        return self.name
    
    @property
    def display_price(self):
        return self.price

    def __str__(self):
        return self.display_name
    
    def get_absolute_url(self):
        return reverse("products:detail",kwargs={'handle':self.handle})
    
    def get_manage_url(self):
        return reverse("products:manage",kwargs={'handle':self.handle})
    
def handle_product_attachment_upload(instance,filename):
    return f"products/{instance.product.handle}/attachments/{filename}"


class ProductAttachment(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    file=models.FileField(upload_to=handle_product_attachment_upload,blank=True,null=True,storage=protected_storage)
    is_free=models.BooleanField(default=False)
    name=models.CharField(max_length=120,null=True,blank=True)
    active=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    # def save(self,*args,**kwargs):
    #     if self.file and not self.name:
    #         self.name=pathlib.Path(self.file.name).name #suffix
    #     super().save(*args,**kwargs)

    @property
    def display_name(self):
        return self.name or pathlib.Path(self.file.name).name
    
    def get_download_url(self):
        return reverse("products:download_attachment",kwargs={'handle':self.product.handle,'pk':self.pk})

