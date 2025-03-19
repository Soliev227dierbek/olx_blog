from django.shortcuts import render, redirect
from .models import Product
from django.db.models import Q
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

def index(request):
    products = Product.objects.all()
    return render(request, 'olx/index.html', {'products':products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'olx/product_detail.html', {'product':product})

def search(request):
    query = request.GET.get('search')
    search_obj = Product.objects.filter(Q(title__iregex = query))
    return render(request, 'olx/search.html', {'search_obj':search_obj, 'query':query})

def create(request):
    if request.method == 'POST':
        product = Product()
        product.title = request.POST.get('title')
        product.text = request.POST.get('text')
        product.price = request.POST.get('price')
        product.save()
        return redirect('index')

def update(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.text = request.POST.get('text')
        product.price = request.POST.get('price')
        product.save()
        return redirect('index')
    return render(request, 'update.html', {'product':product})

def delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
    return redirect('index')
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'olx/register.html', {'form':form})

def login_site(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return render(request, 'olx/login.html', {'error': 'Неверные данные'})
            return render(request, 'olx/login.html')
        return redirect('index')
    
def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')
