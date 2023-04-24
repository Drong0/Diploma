from rest_framework import serializers

from database.models import Vacancy, Favorite, Response, Occupation, Skill, Specialization
from user_auth.models import Company, Client, City, CustomUser, Country
from django.contrib.auth.hashers import make_password

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class OccupationSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'email', 'city', 'first_name', 'last_name', 'phone', 'cv']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class ClientLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = ['email', 'password', 'refresh_token', 'access_token', 'first_name', 'last_name', 'id']
        extra_kwargs = {'password': {'write_only': True}}


class ClientCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = 1
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Client
        fields = ['id','email', 'password', 'city', 'first_name', 'last_name', 'phone', 'refresh_token', 'access_token']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}

    def validate(self, attrs):
        email_exists = CustomUser.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError('Email already exists')
        return super().validate(attrs)

    def create(self, validated_data):
        new_user = Client(**validated_data)

        new_user.password = make_password(validated_data.get('password'))

        new_user.save()

        return new_user


class CompanySerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'company_description', 'city']
        extra_kwargs = {'password': {'write_only': True}, }


class CompanyCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = 2
    company_name = serializers.CharField(max_length=50)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id','email', 'password', 'city', 'company_name', 'company_description', 'refresh_token', 'access_token']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}

    def validate(self, attrs):
        email_exists = CustomUser.objects.filter(email=attrs['email']).exists()
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
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    company_name = serializers.CharField(max_length=255, read_only=True)
    company_description = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'email', 'password', 'company_name', 'refresh_token', 'access_token', 'company_description']
        extra_kwargs = {'password': {'write_only': True}}


class VacancyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    city = CitySerializer(read_only=True)
    occupation = OccupationSerialazer()
    specialization = SpecializationSerializer()

    company = CompanySerializer(read_only=True, many=False)

    class Meta:
        model = Vacancy
        fields = ['name', 'content', 'city', 'salary_min', 'salary_max', 'company', 'company_name',
                  'status', 'occupation', 'specialization', 'id']


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


class ClientProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'email', 'city', 'first_name', 'last_name', 'phone', 'cv']


class CompanyProfileSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id','email', 'city', 'company_name', 'company_description']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
