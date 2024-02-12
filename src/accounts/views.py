from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def registerview(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=CreateUserForm()
        if request.method=="POST":
            form=CreateUserForm(request.POST)
            if form.is_valid:
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,' The account is created for ' + user)
                return redirect('home')
        context={'form':form}
        return render(request,"accounts/register.html",context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                print("failed")
                messages.warning(request,'Username or Password is not valid!!')
        context={}
        return render(request,"accounts/login.html",context)

def logout_user(request):
    logout(request)
    return redirect('accounts:login')