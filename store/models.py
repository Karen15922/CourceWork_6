from django.db import models


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
        return f'{self.pk} - {self.category_name}'

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


class Release(models.Model):
    '''
    модель продуктов
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.01, verbose_name='номер версиии', help_text='Введите номер версии')
    version_name = models.CharField(
        max_length=100, verbose_name='Название версии', help_text='Введите название версии', **NULLABLE)
    is_active = models.BooleanField(
        verbose_name='активная версия', help_text='выберите активную версию')
