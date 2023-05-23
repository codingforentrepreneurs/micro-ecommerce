from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductAttachment

input_css_class = "form-control"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'descriptions', 'price']
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class
            
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'descriptions', 'price']
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class
            
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return price
        
class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = ['file', 'name', 'is_free', 'active']
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class
        
ProductFormAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form=ProductAttachmentForm,
    fields = ['file', 'name', 'is_free', 'active'],
    extra=0,
    can_delete=False
)

ProductFormAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form=ProductAttachmentForm,
    formset= ProductFormAttachmentModelFormSet,
    fields = ['file', 'name', 'is_free', 'active'],
    extra=0,
    can_delete=False
)