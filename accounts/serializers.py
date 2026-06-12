from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','first_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields=('username','first_name','last_name','password','re_password',)
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def validate(self, data):
        password= data.get('password')
        re_password= data.get('re_password')
        if password != re_password:
            raise serializers.ValidationError('Passwords must match')
        return data

    def create(self, validated_data):
        User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
      username= data.get('username')
      password= data.get('password')

      user = authenticate(username=username, password=password)
      if  user is None:
          raise serializers.ValidationError('Invalid username and/or password.')
      return ('user', user)



