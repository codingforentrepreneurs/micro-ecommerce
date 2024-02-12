from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

input_css_class='reg-form'
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            # self.fields[field].widget.attrs['class']=forms.HiddenInput()
            self.fields[field].widget.attrs['class']=input_css_class