from django.http import Http404
from django.shortcuts import render, get_object_or_404
import requests
from django.views.generic import ListView, DetailView
from .models import Category, Product
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
#     paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()

        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        fields = ['id', 'slug', 'name', 'price', 'image', 'category']
        return queryset.only(*fields)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context['category'] = category
        context['categories'] = Category.objects.all()
        context['total_products'] = self.get_queryset().count()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Use select_related() to fetch the related Category object with the
        # product
        return super().get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context
