from django.shortcuts import render, redirect
from .models import Product, Profile, Category, Subcategory
from django.db.models import Q
from .forms import RegisterForm, ProfileForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'olx/index.html', {'products':products, 'categories':categories})

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
        if request.FILES.get('image', False) != False:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            product.image = filename
        product.save()
        return redirect('index')
    return render(request, 'olx/create_product.html')

def update(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.text = request.POST.get('text')
        product.price = request.POST.get('price')
        if request.FILES.get('image', False) != False:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            product.image = filename
        product.save()
        return redirect('index')
    return render(request, 'olx/update.html', {'product':product})

def delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
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
                return redirect('index')
            else:
                return render(request, 'olx/login.html', {'error': 'Nevernoye danniye'})
        return render(request, 'olx/login.html')
    return redirect('index')
    
def logout_site(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile, created = Profile.objects.get_or_create(user=request.user) 
    if request.method == "POST":
        if "delete_profile" in request.POST:
            user = request.user
            profile.delete()
            user.delete()  # Удаляем самого пользователя
            logout(request)  # Разлогиниваем пользователя
            return redirect('index')  # Перенаправляем на главную
        else:
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'olx/profile.html', {'profile': profile, 'form': form})
    
def categories(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'olx/categories.html', {'categories': categories})

def subcategories(request, id):
    subcategory = Subcategory.objects.get(id=id)
    return render(request, 'olx/subcategory.html', {'subcategory': subcategory})
