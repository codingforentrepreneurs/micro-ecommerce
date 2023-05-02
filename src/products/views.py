from django.shortcuts import  render, redirect

# Create your views here.
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.core.cache import cache
from .models import Product
from .forms import ProductForm, ProductUpdateForm

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'
    slug_field = 'handle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.user == self.request.user:
            form = ProductUpdateForm(instance=self.object)
            context['form'] = form
        return context

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
