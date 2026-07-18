from django.urls import path

from .views import (
    CheckoutAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    CancelOrderAPIView,
)

urlpatterns = [

    path(
        "",
        OrderListAPIView.as_view(),
        name="orders",
    ),

    path(
        "checkout/",
        CheckoutAPIView.as_view(),
        name="checkout",
    ),

    path(
        "<int:order_id>/",
        OrderDetailAPIView.as_view(),
        name="order-detail",
    ),

    path(
        "<int:order_id>/cancel/",
        CancelOrderAPIView.as_view(),
        name="cancel-order",
    ),
]