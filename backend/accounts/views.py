from rest_framework import generics
from .serializers import RegisterSerializers
from .models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers