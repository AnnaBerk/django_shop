from django.views.generic import ListView, DetailView
from .models import Product
from cart.forms import CartAddProductForm

from .service import ProductService, CategoryService


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        product_service = ProductService()
        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = product_service.get_products_by_category_slug(category_slug)
        else:
            queryset = product_service.get_all_products()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        if category_slug:
            category = CategoryService.get_category_by_slug(category_slug)
            context['category'] = category
        categories = CategoryService.get_categories()
        context['categories'] = categories
        context['total_products'] = self.get_queryset().count()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context
