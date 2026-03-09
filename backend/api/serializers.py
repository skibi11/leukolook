from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import EyeTestResult

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Expose whichever fields you need
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id', 'is_active']
        
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        attrs['email'] = attrs.get('email').lower()
        return super().validate(attrs)
    
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # use create_user to ensure password is hashed
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

class EyeTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EyeTestResult
        fields = [
            'id',
            'user',
            'created_at',
            'original',
            'left_eye',
            'right_eye',
            'has_leukocoria_left',
            'has_leukocoria_right',
        ]
        read_only_fields = ['id', 'user', 'created_at']
