from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,ProductAttachment
import mimetypes
from django.http import HttpResponseBadRequest,FileResponse
from .forms import ProductForm,ProductUpdateForm,ProductAttachmentModelFormset,ProductAttachmentInlineFormset
# from django.contrib.auth import authenticate,get_user,base_user

# Create your views here.
def product_create_view(request):
    context={}
    form=ProductForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        if request.user.is_authenticated:
            obj.user=request.user
            obj.save()
            return redirect(obj.get_manage_url())
        else:
            form.add_error(None,"User must be logged in")

    context['form']=form
    return render(request,'products/create.html',context)

def product_list_view(request):
    obj_list=Product.objects.all()
    return render(request,'products/list.html',{'objects':obj_list})


def product_detail_view(request,handle=None):
    obj=get_object_or_404(Product,handle=handle)
    attachments=ProductAttachment.objects.filter(product=obj)
    # attachments=obj.productattachmentset.all()
    is_owner=False
    if request.user.is_authenticated:
        is_owner=request.user.purchase_set.all().filter(product=obj,completed=True).exists()
    context={'obj':obj,'is_owner':is_owner,'attachments':attachments,'product':Product}
    return render(request,'products/detail.html',context)


# def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False

    if request.user.is_authenticated:
        is_manager = obj.user == request.user

    context = {'obj': obj}

    if not is_manager:
        return HttpResponseBadRequest()

    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineFormset(request.POST or None, queryset=attachments)

    if form.is_valid() and formset.is_valid():
        # Save the product instance
        form.save()

        # Save the formset instances
        for attachment_obj in formset:
            attachment_obj.product = obj
            attachment_obj.save()

        return redirect(obj.get_manage_url())

    context['form'] = form
    context['formset'] = formset

    return render(request, 'products/manager.html', context)

def product_manage_detail_view(request,handle=None):
    obj=get_object_or_404(Product,handle=handle)
    attachments=ProductAttachment.objects.filter(product=obj)
    is_manager=False
    if request.user.is_authenticated:
        is_manager=obj.user==request.user
    context={'obj':obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form=ProductUpdateForm(request.POST or None,request.FILES or None,instance=obj)
    formset=ProductAttachmentInlineFormset(request.POST or None,queryset=attachments)
    if form.is_valid() or formset.is_valid():
            print(attachments)
            instance=form.save(commit=False)
            instance.save()
            attachment_obj=formset.save(commit=False)
            attachment_obj.save()
            return redirect(obj.get_manage_url())
    context['form']=form
    context['formset']=formset
    return render(request,'products/manager.html',context)

def product_attachment_download_view(request,handle=None,pk=None):
    attachment=get_object_or_404(ProductAttachment,product__handle=handle,pk=pk)
    can_download=attachment.is_free or False
    if request.user.is_authenticated:
        can_download=True
    if can_download is False:
        return HttpResponseBadRequest()
    file=attachment.file.open(mode='rb')
    filename=attachment.file.name
    content_type=mimetypes.guess_type(filename)
    response=FileResponse(file)
    response['Content-Type']=content_type or 'application/octet-stream'
    response['Content-Disposition']=f'attachment;filename={file.name}'
    return response
