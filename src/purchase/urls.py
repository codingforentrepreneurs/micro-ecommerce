from django.urls import path

from purchase import views

app_name='purchase'
urlpatterns=[
    path('start/',views.purchase_start_view,name='start'),
    path('success/',views.purchase_success_view,name='success'),
    path('stopped/',views.purchase_stopped_view,name='stopped'),

]