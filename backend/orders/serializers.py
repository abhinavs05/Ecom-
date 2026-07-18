from decimal import Decimal

from rest_framework import serializers

from .models import Order, OrderItem


class CheckoutSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField(required=False)


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "sku",
            "quantity",
            "unit_price",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "subtotal",
            "discount",
            "tax",
            "shipping_charge",
            "total_amount",
            "payment_status",
            "created_at",
            "items",
        ]