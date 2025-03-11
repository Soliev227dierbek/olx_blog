from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product_detail/<slug:slug>', views.product_detail, name='product_detail_url'),
    path('search/', views.search, name='search'),
]