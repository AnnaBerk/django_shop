from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm
from .service import CartService


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    cart_form = CartAddProductForm(request.POST)
    if cart_form.is_valid():
        cleaned_data = cart_form.cleaned_data
        CartService().add_to_cart(cart, product_id, cleaned_data['quantity'], cleaned_data['update'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    CartService().remove_from_cart(cart, product_id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
