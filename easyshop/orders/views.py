from django.shortcuts import render
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.service import OrderService

from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        try:
            order = OrderService.create_order(request, form, cart)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
        except Exception as e:
            # Handle exception
            pass
    else:
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})
