from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import User , Profile

class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "password",
            "first_name",
            "last_name",
        ]

    def create(self , validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only = True)
    email = serializers.EmailField(source="user.email", read_only = True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    phone_number = serializers.CharField(source="user.phone_number", required=False)

    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "dob",
            "gender",
        ]
    
    def update(self,instance,validated_data):
        user_data = validated_data.pop("user",{})

        user = instance.user

        for attr ,value in user_data.items():
            setattr(user,attr,value)
        
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance