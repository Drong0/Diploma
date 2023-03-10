from rest_framework import serializers

from database.models import Vacancy, Favorite, Response
from user_auth.models import Company, Client
from django.contrib.auth.hashers import make_password


class ClientSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'token', 'email', 'city_name', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class ClientLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        model = Client
        fields = ['email', 'password']


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
        fields = ['id', 'token', 'company_name', 'company_description', 'city']
        extra_kwargs = {'password': {'write_only': True}, }


class CompanyCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = 2
    company_name = serializers.CharField(max_length=50)

    class Meta:
        model = Company
        fields = ['email', 'password', 'city', 'company_name', 'company_description']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}

    def validate(self, attrs):
        email_exists = Client.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError('Email already exists')
        return super().validate(attrs)

    def create(self, validated_data):
        new_user = Company(**validated_data)

        new_user.password = make_password(validated_data.get('password'))
        new_user.user_type = 2

        new_user.save()

        return new_user


class CompanyLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        model = Company
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class VacancyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    city_name = serializers.CharField(source='city.city', read_only=True)
    occupation_name = serializers.CharField(source='occupation.name')
    specialization_name = serializers.CharField(source='specialization.name')

    company = CompanySerializer(read_only=True, many=False)

    class Meta:
        model = Vacancy
        fields = ['name', 'content', 'city', 'city_name', 'salary_min', 'salary_max', 'company', 'company_name',
                  'status', 'occupation_name', 'specialization_name', 'id']


class FavoriteSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(read_only=True, many=False)
    client = ClientSerializer(read_only=True, many=False)

    class Meta:
        model = Favorite
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(read_only=True, many=False)
    client = ClientSerializer(read_only=True, many=False)

    class Meta:
        model = Response
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'email', 'city', 'first_name', 'city_name', 'last_name', 'phone', 'cv']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
