from rest_framework import serializers

from database.models import Vacancy, Favorite, Response
from user_auth.models import Company, Client
from django.contrib.auth.hashers import make_password


class ClientSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'token', 'email', 'user_type', 'city', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class ClientLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        model = Client
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class ClientCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = 1
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)

    class Meta:
        model = Client
        fields = ['email', 'password', 'city', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}

    def validate(self, attrs):
        email_exists = Client.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError('Email already exists')
        return super().validate(attrs)

    def create(self, validated_data):
        new_user = Client(**validated_data)

        new_user.password = make_password(validated_data.get('password'))

        new_user.save()

        return new_user


class CompanySerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'token', 'company_name', 'company_description', 'user_type', 'city']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class CompanyCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = serializers.IntegerField(default=2)
    company_name = serializers.CharField(max_length=50)

    class Meta:
        model = Company
        fields = ['email', 'password', 'city', 'company_name', 'user_type']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}

    def validate(self, attrs):
        email_exists = Client.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError('Email already exists')
        return super().validate(attrs)

    def create(self, validated_data):
        new_user = Company(**validated_data)

        new_user.password = make_password(validated_data.get('password'))

        new_user.save()

        return new_user


class CompanyLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        model = Company
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'
