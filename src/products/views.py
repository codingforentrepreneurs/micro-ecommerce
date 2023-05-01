from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.core.cache import cache
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'handle'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.object.user == self.request.user:
    #         form = ProductForm(instance=self.object)
    #         context['form'] = form
    #     return context

    # def post(self, request):
    #     self.object = self.get_object()
    #     if self.object.user == request.user:
    #         form = ProductForm(request.POST, instance=self.object)
    #         if form.is_valid():
    #             form.save()
    #     return self.render_to_response(self.get_context_data())

def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = obj.user == request.user
    context = {"object": obj}
    if is_owner:
        form = ProductForm(request.POST or None, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            # return redirect('/products/create/')
        context['form'] = form
    return render(request, 'products/detail.html', context)
    
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('products:product_list_class')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            cache.clear()
            return super().form_valid(form)
        else:
            form.add_error(None, 'User is not authenticated')
            return self.form_invalid(form)

def product_create_view(request):
    context  = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            cache.clear()
            obj.save()
            return redirect('products:product_create')
        else:
            form.add_error(None, "User is not authenticated")
        
    context['form'] = form
    return render(request, 'products/create.html', context)
