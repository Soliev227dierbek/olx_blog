from django.contrib import admin
from .models import Product

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Product, SlugAdmin)
# Register your models here.
