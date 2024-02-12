from django.urls import path

from . import views
app_name="accounts"
urlpatterns=[
    path('login/',views.login_view,name="login"),
    path('register/',views.registerview,name="register"),
    path('logout/',views.logout_user,name='logout')
]