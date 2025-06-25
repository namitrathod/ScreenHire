from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Applicant, JobListings, Application

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','role']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','password']
    def create(self, validated_data):
        user = User(email=validated_data['email'], role='JOBSEEKER')
        user.set_password(validated_data['password'])
        user.save()
        Applicant.objects.create(user=user)
        return user

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListings
        fields = ['id','title','department','posted_date']
