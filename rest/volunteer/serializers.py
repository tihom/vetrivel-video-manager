from django.contrib.auth.models import User
from .models import Volunteer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'first_name', 'last_name',)

class VolunteerSerializer(serializers.ModelSerializer):
    # field from the user model
    id = serializers.CharField(source='user.id', required=False)
    name = serializers.CharField(source='user.username', required=True)
    email = serializers.CharField(source='user.email', required=True)
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)

    class Meta:
        model = Volunteer
        fields = ('id', 'name', 'email', 'first_name', 'last_name',
            'phone', 'leader') 
