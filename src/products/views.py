import mimetypes
from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import  get_object_or_404, render, redirect

# Create your views here.
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from .models import Product, ProductAttachment
from .forms import ProductForm, ProductUpdateForm, ProductFormAttachmentInlineFormSet

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

def product_create_view(request):
    context  = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('products:product_create')
        else:
            form.add_error(None, "User is not authenticated")
        
    context['form'] = form
    return render(request, 'products/create.html', context)

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('products:product_list_class')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            form.add_error(None, 'User is not authenticated')
            return self.form_invalid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # template_name = 'products/update.html'
    form_class = ProductUpdateForm
    slug_field = 'handle'
    
    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'slug': self.object.handle})

    def form_valid(self, form):
        if self.object.user == self.request.user:
            form.save()
        return super().form_valid(form)
        
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
    formset = ProductFormAttachmentInlineFormSet(request.POST or None, 
                                            request.FILES or None,
                                            queryset=attachments)
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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'handle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        attachments = ProductAttachment.objects.filter(product=obj)
        is_owner = False
        if self.request.user.is_authenticated:
            # is_owner = True
            is_owner = self.request.user.purchase_set.all().filter(product=obj, completed=True).exists()
        context["is_owner"] = is_owner
        context["attachments"] = attachments
        return context

def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True # check ownership
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb') # cdn -> S3 object storage
    filename = attachment.file.name
    content_type, _ = mimetypes.guess_type(filename)
    response =  FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response

