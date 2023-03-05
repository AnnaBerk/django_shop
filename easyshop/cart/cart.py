from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    """
    A shopping cart object that stores items in a session
    """

    def __init__(self, request):
        """
        Initializes the cart object and creates an empty cart in the session if it doesn't exist
        :param request: the HTTP request object
        """
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})
        if not self.cart:
            self.session[settings.CART_SESSION_ID] = self.cart

    def __iter__(self):
        """
        Iterates over the items in the cart and retrieves the corresponding products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            product_id = str(product.id)
            self.cart[product_id]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Returns the total number of items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())


    def add(self, product, quantity=1, update_quantity=False):
        """
        Adds a product to the cart or updates its quantity
        :param product: the product instance to add or update
        :param quantity: the quantity to add or update (default 1)
        :param update_quantity: whether to update the quantity instead of adding to it (default False)
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Removes a product from the cart
        :param product: the product to remove
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Calculates the total price of all items in the cart
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Clears the cart by removing it from the session
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def save(self):
        """
        Saves the cart to the session and marks the session as modified
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True