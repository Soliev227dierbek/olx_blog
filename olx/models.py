from django.db import models
from django.shortcuts import reverse

class Product(models.Model):
    title = models.CharField('Название', max_length=255)
    text = models.TextField('Текст')
    image = models.ImageField('Фото', blank=True, null=True)
    price = models.IntegerField('Цена', default=0)

    def get_link(self):
        return reverse('product_detail_url', kwargs = {'id':self.id})
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
# Create your models here.
