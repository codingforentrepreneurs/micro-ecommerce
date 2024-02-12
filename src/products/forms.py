from collections.abc import Mapping
from typing import Any
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Product,ProductAttachment
from django import forms
from django.forms import inlineformset_factory,modelformset_factory,HiddenInput
from django.contrib.auth.models import User

input_css_class='form-control'
# label_class='labelling'
input_css_class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

class ProductForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    class Meta:
        model=Product
        fields={
            'name',
            'handle',
            'price'
        }
    field_order=['name','handle','price']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            # self.fields['label'].widget.attrs['class']=label_class
            self.fields[field].widget.attrs['class']=input_css_class
    

class ProductUpdateForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    class Meta:
        model=Product
        fields={
            'image',
            'name',
            'handle',
            'price'
        }
        field_order=['name','handle','price','image']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            # self.fields['label'].widget.attrs['class']=label_class
            self.fields[field].widget.attrs['class']=input_css_class


class ProductAttachmentForm(forms.ModelForm):
    # name=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))
    class Meta:
        model=ProductAttachment
        fields=[
            'file',
            'name',
            'active',
            'is_free'
        ]
        
        # field_order=['name','handle','price','file']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            if field in ['active','is_free']:
                continue
            # self.fields['label'].widget.attrs['class']=label_class
            self.fields[field].widget.attrs['class']=input_css_class
        


ProductAttachmentModelFormset=modelformset_factory(
                                                ProductAttachment,
                                                    form=ProductAttachmentForm,
                                                   fields=['file','name','is_free','active'],
                                                   extra=0,
                                                   can_delete=False)

ProductAttachmentInlineFormset=inlineformset_factory(Product,
                                                    ProductAttachment,
                                                    form=ProductAttachmentForm,
                                                    formset=ProductAttachmentModelFormset,
                                                    fields=['file','name','is_free','active'],
                                                    extra=0,
                                                    can_delete=True)

