from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializer import (
    AddToCartSerializer,
    UpdateCartItemSerializer,
    CartSerializer,
)

from .services import (
    get_cart,
    add_to_cart,
    update_cart_item,
    remove_from_cart,
)


class CartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = get_cart(request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AddToCartSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:

            add_to_cart(
                request.user,
                serializer.validated_data["product_id"],
                serializer.validated_data["quantity"],
            )

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = get_cart(request.user)

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_201_CREATED,
        )


class UpdateCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, cart_item_id):

        serializer = UpdateCartItemSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:

            update_cart_item(
                request.user,
                cart_item_id,
                serializer.validated_data["quantity"],
            )

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            CartSerializer(get_cart(request.user)).data
        )


class RemoveCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_item_id):

        remove_from_cart(
            request.user,
            cart_item_id,
        )

        return Response(
            CartSerializer(get_cart(request.user)).data
        )