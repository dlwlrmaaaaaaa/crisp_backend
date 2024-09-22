from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Citizen, Workers, DepartmentAdmin

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.utils import get_account_type

class CitizenSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)  # Accept user identifier
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Hide password input
    

    class Meta:
        model = Citizen
        fields = ['user', 'password', 'address', 'contact_number']

    def validate_contact_number(self, value):
        if Citizen.objects.filter(contact_number=value).exists():
            raise serializers.ValidationError("This contact number is already in use.")
        return value

    def validate_user(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists!")
        return value

    def create(self, validated_data):
        user_identifier = validated_data.pop('user')
        password = validated_data.pop('password')

        user = User(username=user_identifier)
        user.set_password(password)
        user.save()

        citizen = Citizen.objects.create(user=user, **validated_data)
        return citizen
    
class WorkersSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)  # Accept user identifier
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Hide password input

    class Meta:
        model = Workers
        fields = ['user', 'password', 'contact_number']

    def validate_contact_number(self, value):
        if Workers.objects.filter(contact_number=value).exists():
            raise serializers.ValidationError("This contact number is already in use.")
        return value

    def validate_user(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists!")
        return value

    def create(self, validated_data):
        user_identifier = validated_data.pop('user')
        password = validated_data.pop('password')

        user = User(username=user_identifier)
        user.set_password(password)
        user.save()

        worker = Workers.objects.create(user=user, **validated_data)
        return worker
    
class DepartmentHeadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(write_only=True)  # Accept user identifier
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})  # Hide password input

    class Meta:
        model = DepartmentAdmin
        fields = ['user', 'password', 'contact_number', 'department', 'address']

    def validate_contact_number(self, value):
        if DepartmentAdmin.objects.filter(contact_number=value).exists():
            raise serializers.ValidationError("This contact number is already in use.")
        return value

    def validate_user(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists!")
        return value

    def create(self, validated_data):
        user_identifier = validated_data.pop('user')
        password = validated_data.pop('password')

        user = User(username=user_identifier)
        user.set_password(password)
        user.save()

        departmentadmin = DepartmentAdmin.objects.create(user=user, **validated_data)
        return departmentadmin
    
# ito bago 
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Get the user account type
        account_type = get_account_type(self.user)

        # Add the account type to the token response
        data['account_type'] = account_type

        return data
    

    

# class DepartmentAdmin(serializers.ModelSerializer):
