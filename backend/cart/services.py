from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from catalog.models import Product


def get_cart(user):
    """
    Returns the user's cart.
    Creates one if it doesn't exist.
    """

    cart, _ = Cart.objects.get_or_create(user=user)

    return cart


@transaction.atomic
def add_to_cart(user, product_id, quantity):

    cart = get_cart(user)

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    if product.stock < quantity:
        raise ValueError("Not enough stock available.")

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )

    if not created:

        new_quantity = cart_item.quantity + quantity

        if new_quantity > product.stock:
            raise ValueError("Requested quantity exceeds stock.")

        cart_item.quantity = new_quantity
        cart_item.save()

    return cart_item


@transaction.atomic
def update_cart_item(user, cart_item_id, quantity):

    cart = get_cart(user)

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=cart,
    )

    if quantity > cart_item.product.stock:
        raise ValueError("Not enough stock.")

    cart_item.quantity = quantity
    cart_item.save()

    return cart_item


@transaction.atomic
def remove_from_cart(user, cart_item_id):

    cart = get_cart(user)

    cart_item = get_object_or_404(
        CartItem,
        id=cart_item_id,
        cart=cart,
    )

    cart_item.delete()


@transaction.atomic
def clear_cart(user):

    cart = get_cart(user)

    cart.items.all().delete()


def calculate_cart_total(cart):

    subtotal = Decimal("0.00")

    for item in cart.items.select_related("product"):

        subtotal += (
            item.product.price *
            item.quantity
        )

    return subtotal


def get_cart_summary(user):

    cart = get_cart(user)

    subtotal = calculate_cart_total(cart)

    total_items = sum(
        item.quantity
        for item in cart.items.all()
    )

    return {
        "cart": cart,
        "subtotal": subtotal,
        "total_items": total_items,
    }