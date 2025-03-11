from django.shortcuts import render
from .models import Product
from django.db.models import Q

def index(request):
    products = Product.objects.all()[:3]
    return render(request, 'olx/index.html', {'products':products})

def product_detail(request, slug):
    product = Product.objects.get(slug__iexact = slug)
    return render(request, 'olx/product_detail.html', {'product':product})

def search(request):
    query = request.GET.get('search')
    search_obj = Product.objects.filter(Q(title__iregex = query))
    return render(request, 'olx/search.html', {'search_obj':search_obj, 'query':query})
# Create your views here.
