from django.contrib import admin
from django.urls import path,include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('submit/',views.submit),
    path('home/<str:status>',views.home),
    path('search/',views.search),
    path('<int:contact>/generate/',views.generateID),
    re_path(r'^accounts/login/$', LoginView.as_view(), name='login'), #Addlogin authentication
    re_path(r'^logout/$', LogoutView.as_view(), {'next_page': '/login/'}, name='logout'), #Logout
    path('register/', views.register),
]
