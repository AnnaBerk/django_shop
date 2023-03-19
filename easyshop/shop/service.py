from django.shortcuts import get_object_or_404
from .models import Product, Category
from typing import List

from shop.models import Category
class ProductService:
    def get_all_products(self):
        fields = ['id', 'slug', 'name', 'price', 'image', 'category']
        return Product.products.only(*fields)

    def get_product_by_slug(self, slug):
        fields = ['id', 'slug', 'name', 'price', 'image', 'category']
        product = get_object_or_404(Product.products.only(*fields), slug=slug)
        return product

    def get_products_by_category_slug(self, category_slug):

        return Product.products.filter(category__slug=category_slug)


class CategoryService:
    @staticmethod
    def get_categories() -> List[Category]:
        return Category.objects.all()

    @staticmethod
    def get_category_by_slug(slug: str) -> Category:
        return get_object_or_404(Category, slug=slug)