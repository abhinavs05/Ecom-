from django.urls import path

from .views import (
    CartAPIView,
    AddToCartAPIView,
    UpdateCartItemAPIView,
    RemoveCartItemAPIView,
)

urlpatterns = [

    path(
        "",
        CartAPIView.as_view(),
        name="cart",
    ),

    path(
        "items/",
        AddToCartAPIView.as_view(),
        name="add-to-cart",
    ),

    path(
        "items/<int:cart_item_id>/",
        UpdateCartItemAPIView.as_view(),
        name="update-cart-item",
    ),

    path(
        "items/<int:cart_item_id>/delete/",
        RemoveCartItemAPIView.as_view(),
        name="remove-cart-item",
    ),
]