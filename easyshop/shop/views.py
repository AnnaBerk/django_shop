
from django.http import Http404
from django.shortcuts import render, get_object_or_404
import requests
from django.views.generic import ListView, DetailView
from .models import Category, Product


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('category_slug'):
            category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            queryset = queryset.filter(category=category)
        queryset = queryset.filter(available=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            context['category'] = category
            context['products'] = Product.objects.filter(category=category, available=True)
        else:
            context['products'] = Product.objects.filter(available=True)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(available=True)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.available:
            raise Http404("Product does not exist")
        return obj


# def load_products(request):
#     r = requests.get('https://fakestoreapi.com/products')
#     for item in r.json():
#         product = Product(
#             name=item['title'],
#             description=item['description'],
#             price=item['price'],
#             image=item['image'],
#             stock=10,
#         )
#         product.save()
#     return render(request, 'shop/product/list.html')