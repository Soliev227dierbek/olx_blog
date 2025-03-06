from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()[:3]
    return render(request, 'olx/index.html', {'products':products})

def product_detail(request, slug):
    product = Product.objects.get(slug__iexact = slug)
    return render(request, 'olx/product_detail.html', {'product':product})
# Create your views here.
