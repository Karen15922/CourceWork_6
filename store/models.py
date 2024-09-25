from django.db import models
from users.models import User


# константа для полей с возможно нулевыми значениями
NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    '''
    модель категорий
    '''
    category_name = models.CharField(
        max_length=100, verbose_name='название категории')
    description = models.TextField(
        max_length=500, verbose_name='описание категории')

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    '''
    модель продуктов
    '''
    product_name = models.CharField(
        max_length=100, verbose_name='название продукта',)
    description = models.TextField(
        max_length=500, verbose_name='описание продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(**NULLABLE)
    price = models.DecimalField(max_digits=6, decimal_places=2, **NULLABLE)

    def __str__(self):
        return f'{self.product_name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Views(models.Model):
    '''
    модель просмотров
    '''
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'просмотр'
        verbose_name_plural = 'просмотры'
