from django.db import transaction
from orders.models import OrderItem
from orders.tasks import order_created


class OrderService:
    @staticmethod
    def create_order(request, form, cart):
        if form.is_valid():
            order = form.save()
            OrderService.create_order_items(order, cart)
            cart.clear()
            order_created.delay(order.id)
            return order
        else:
            raise Exception('Invalid form data')

    @staticmethod
    @transaction.atomic
    def create_order_items(order, cart):
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )