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
# Create your models here.
