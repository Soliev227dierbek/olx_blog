from django.contrib import admin
from .models import Product, Profile, Category, Subcategory

admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Subcategory)

# Register your models here.
