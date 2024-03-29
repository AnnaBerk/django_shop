from _decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r})')

    def __str__(self):
        return self.name


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True).select_related('category')


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    products = ProductManager()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r}, {self.category!r})')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


