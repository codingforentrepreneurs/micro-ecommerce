from django.urls import path

from . import views
from .views import ProductCreateView, ProductDetailView, ProductListView, ProductUpdateView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_class'),
    path('create/', views.product_create_view, name='product_create'),
    path('create_class/', ProductCreateView.as_view(), name='product_create_class'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:handle>/manage/', views.product_manage_detail_view, name='product_manage'),
    path('<slug:handle>/download/<int:pk>', views.product_attachment_download_view, name='download'),
    path('<slug:slug>/update/', ProductUpdateView.as_view(), name='product_update'),
]
