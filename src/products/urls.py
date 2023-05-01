from django.urls import path

from . import views
from .views import ProductCreateView, ProductDetailView, ProductListView, ProductUpdateView
# from django.views.decorators.cache import cache_page

app_name = 'products'
urlpatterns = [
    # path('', cache_page(60 * 15, key_prefix='product_list')(ProductListView.as_view()), name='product_list_class'),
    path('', ProductListView.as_view(), name='product_list_class'),
    path('create/', views.product_create_view, name='product_create'),
    path('create_class/', ProductCreateView.as_view(), name='product_create_class'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
]
