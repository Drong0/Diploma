from rest_framework import serializers

from database.models import Vacancy, Favorite, Response, Occupation, Skill, Specialization
from user_auth.models import Company, Client, City, CustomUser
from django.contrib.auth.hashers import make_password


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
    token = serializers.CharField(max_length=255, read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'token', 'email', 'city', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'password': {'write_only': True}, 'user_type': {'read_only': True}}


class ClientLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    token = TokenSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['email', 'password', 'token']


class ClientCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = 1
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)
    token = TokenSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['email', 'password', 'city', 'first_name', 'last_name', 'phone', 'token']
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
    token = serializers.CharField(max_length=255, read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'token', 'company_name', 'company_description', 'city']
        extra_kwargs = {'password': {'write_only': True}, }


class CompanyCreateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, required=True)
    user_type = 2
    company_name = serializers.CharField(max_length=50)
    token = TokenSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['email', 'password', 'city', 'company_name', 'company_description', 'token']
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
        fields = "__all__"


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
