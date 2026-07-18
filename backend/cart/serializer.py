from decimal import Decimal

from rest_framework import serializers

from .models import Cart, CartItem
from catalog.models import Product


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, available=True).exists():
            raise serializers.ValidationError("Product does not exist.")

        return value


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)


class CartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(source="product.id", read_only=True)

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_image = serializers.ImageField(
        source="product.image",
        read_only=True
    )

    unit_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem

        fields = [
            "id",
            "product_id",
            "product_name",
            "product_image",
            "unit_price",
            "quantity",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    subtotal = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = [
            "id",
            "total_items",
            "subtotal",
            "items",
            "created_at",
            "updated_at",
        ]

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_subtotal(self, obj):

        total = Decimal("0.00")

        for item in obj.items.select_related("product"):
            total += item.product.price * item.quantity

        return total