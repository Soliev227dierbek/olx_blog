from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('categories/', views.categories, name='categories'),
    path('subcategories/<int:id>', views.subcategories, name='subcategories'),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'), 
    path('register/', views.register, name='register'),
    path('login/', views.login_site, name='login'),
    path('logout/', views.logout_site, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('favorites/add/<int:id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:id>/', views.remove_from_favorites, name='remove_from_favorites'),
]