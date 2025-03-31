from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField('Название', max_length=255)
    text = models.TextField('Текст')
    image = models.ImageField('Фото', blank=True, null=True)
    price = models.IntegerField('Цена', default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    name = models.CharField('Название Категории',max_length=255, unique=True)

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
# Create your models here.
#unique=True в Django означает, что значение этого поля должно быть уникальным среди всех записей в таблице базы данных.