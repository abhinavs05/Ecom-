from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    OrderSerializer,
)

from .services import (
    create_order,
    get_user_orders,
    get_order,
    cancel_order,
)


class CheckoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            order = create_order(request.user)

            serializer = OrderSerializer(order)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = get_user_orders(request.user)

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)


class OrderDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):

        order = get_order(
            request.user,
            order_id
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class CancelOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):

        try:

            order = cancel_order(
                request.user,
                order_id
            )

            serializer = OrderSerializer(order)

            return Response(serializer.data)

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )