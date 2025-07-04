from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('Название Категории',max_length=255, unique=True)
    image = models.ImageField('Иконка', default='None')

    def __str__(self):
        return self.name

class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CHOICES = [
        ('Новый','Новый'),
        ('Б/У','Б/У'),
    ]
    def get_default_subcategory():
        default_subcategory = Subcategory.objects.first()
        return default_subcategory.id if default_subcategory else None
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField('Название', max_length=255, blank=False)
    text = models.TextField('Текст')
    image = models.ImageField('Фото', blank=True, null=True)
    image2 = models.ImageField('Фото 2', blank=True, null=True, upload_to='photo_2/')
    image3 = models.ImageField('Фото 3', blank=True, null=True, upload_to='photo_3/')
    price = models.IntegerField('Цена', default=0)
    condition = models.CharField('Состояние', max_length=10, choices=CONDITION_CHOICES, default='Новый')
    date = models.DateTimeField('Дата выпуска', default = timezone.now)
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name = 'Категория', default = get_default_subcategory)
    
    def name(self):
        return self.title

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Имя', max_length=255)
    avatar = models.ImageField('Фото профиля', upload_to='avatars/')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField('Местонахождение', max_length=100, default='Не указано')

    def __str__(self):
        return self.user.username
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='None')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    

class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.user} -> {self.product}"
    
    class Meta:
        unique_together = ('user', 'product') 

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1-5

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}/5"
    
# Create your models here.
#unique=True в Django означает, что значение этого поля должно быть уникальным среди всех записей в таблице базы данных.