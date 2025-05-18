from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Profile, Category, Subcategory, Cart, Favorite
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'olx/register.html', {'form': form})

# Авторизация
def login_site(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'olx/login.html', {
                'error': 'Неверное имя пользователя или пароль'
            })

    return render(request, 'olx/login.html')

# Выход из аккаунта
@login_required
def logout_site(request):
    logout(request)
    return redirect('index')

# Профиль пользователя
@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if "delete_profile" in request.POST:
            request.user.delete()
            logout(request)
            return redirect('index')
        else:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'olx/profile.html', {
        'profile': profile,
        'form': form
    })

    
def categories(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'olx/categories.html', {'categories': categories})

def subcategories(request, id):
    subcategory = Subcategory.objects.get(id=id)
    return render(request, 'olx/subcategory.html', {'subcategory': subcategory})

# Просмотр корзины
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)  # Убедись, что метод total_price есть в модели Cart
    return render(request, 'olx/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# Добавить товар в корзину
@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    item, created = Cart.objects.get_or_create(user=request.user, product=product)
    item.quantity += 1
    item.save()
    return redirect('cart_view')

# Уменьшить количество товара в корзине
@login_required
def decrease_quantity(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # Удалить, если количество становится 0
    return redirect('cart_view')

# Удалить товар из корзины
@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart_view')

# Обновление профиля пользователя
@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление после сохранения
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'olx/update_profile.html', {
        'form': form,
        'profile': profile
    })

# Добавить товар в избранное
@login_required
def add_to_favorites(request, id):
    product = get_object_or_404(Product, id=id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    return redirect('favorites')

# Удалить товар из избранного
@login_required
def remove_from_favorites(request, id):
    product = get_object_or_404(Product, id=id)
    favorite = Favorite.objects.filter(user=request.user, product=product)
    favorite.delete()
    return redirect('favorites')

# Просмотр списка избранных товаров
@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'olx/favorites.html', {
        'favorites': favorites
    })
