from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail_url'),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('register/', views.register, name='register'),
    path('login/', views.login_site, name='login'),
    path('logout/', views.logout_site, name='logout'),
    path('profile/', views.profile, name='profile'),
]