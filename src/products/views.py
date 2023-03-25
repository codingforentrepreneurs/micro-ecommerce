import mimetypes

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from cfehome.storages.utils import generate_presigned_url
# Create your views here.
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormSet
from .models import Product, ProductAttachment


def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect(obj.get_manage_url())
        form.add_error(None, "Your must be logged in to create products.")
    context['form'] = form
    return render(request, 'products/create.html', context)

def product_list_view(request):
    object_list = Product.objects.all()
    return render(request, "products/list.html", {"object_list": object_list})



def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineFormSet(request.POST or None, 
                                             request.FILES or None,queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None
            if is_delete:
                if attachment_obj is not None:
                    if attachment_obj.pk:
                        attachment_obj.delete()
            else:
                if attachment_obj is not None:
                    attachment_obj.product  = instance
                    attachment_obj.save()
        return redirect(obj.get_manage_url())
    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manager.html', context)

def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    # attachments = obj.productattachment_set.all()
    is_owner = False
    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.all().filter(product=obj, completed=True).exists()
    context = {"object": obj, "is_owner": is_owner, "attachments": attachments}
    return render(request, 'products/detail.html', context)

def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated and can_download is False:
        can_download = request.user.purchase_set.all().filter(product=attachment.product, completed=True).exists()
    if can_download is False:
        return HttpResponseBadRequest()
    file_name = attachment.file.name # .open(mode='rb') # cdn -> S3 object storage
    file_url = generate_presigned_url(file_name)
    # filename = attachment.file.name
    # content_type, _ = mimetypes.guess_type(filename)
    # response =  FileResponse(file)
    # response['Content-Type'] = content_type or 'application/octet-stream'
    # response['Content-Disposition'] = f'attachment;filename={filename}'
    return HttpResponseRedirect(file_url)