from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from cart.models import Cart
from catalog.models import Product
from .models import Order, OrderItem


TAX_RATE = Decimal("0.18")
SHIPPING_CHARGE = Decimal("100.00")


def calculate_subtotal(cart):
    subtotal = Decimal("0.00")

    for item in cart.items.select_related("product"):
        subtotal += item.product.price * item.quantity

    return subtotal


@transaction.atomic
def create_order(user):

    cart = get_object_or_404(
        Cart.objects.prefetch_related("items__product"),
        user=user
    )

    cart_items = cart.items.all()

    if not cart_items.exists():
        raise ValueError("Cart is empty.")

    subtotal = calculate_subtotal(cart)

    tax = subtotal * TAX_RATE

    total_amount = subtotal + tax + SHIPPING_CHARGE

    order = Order.objects.create(
        user=user,
        subtotal=subtotal,
        tax=tax,
        shipping_charge=SHIPPING_CHARGE,
        total_amount=total_amount,
        payment_status="PENDING",
    )

    for item in cart_items:

        if item.quantity > item.product.stock:
            raise ValueError(
                f"{item.product.name} is out of stock."
            )

        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            sku="",                     # Replace with item.product.sku later
            quantity=item.quantity,
            unit_price=item.product.price,
            total_price=item.product.price * item.quantity,
        )

        product = item.product
        product.stock -= item.quantity
        product.save()

    cart.items.all().delete()

    return order


def get_user_orders(user):

    return Order.objects.filter(
        user=user
    ).prefetch_related("items")


def get_order(user, order_id):

    return get_object_or_404(
        Order.objects.prefetch_related("items"),
        id=order_id,
        user=user,
    )


@transaction.atomic
def cancel_order(user, order_id):

    order = get_order(user, order_id)

    if order.status != Order.Status.PENDING:
        raise ValueError(
            "Only pending orders can be cancelled."
        )

    order.status = Order.Status.CANCELLED
    order.save()

    for item in order.items.all():

        product = item.product

        product.stock += item.quantity

        product.save()

    return order


def update_order_status(order, status):

    order.status = status
    order.save()

    return order