from django.shortcuts import get_object_or_404
from shop.models import Product
from .cart import Cart

class CartService:
    @staticmethod
    def add_to_cart(self, cart: Cart, product_id: int, quantity: int, update: bool):
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity, update_quantity=update)

    @staticmethod
    def remove_from_cart(self, cart: Cart, product_id: int):
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
