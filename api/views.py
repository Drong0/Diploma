from django.contrib.auth import authenticate
from rest_framework import status, permissions, generics, viewsets, filters
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import VacancyFilter
from api.serializers import (ClientLoginSerializer,
                             ClientCreateSerializer,
                             CompanyLoginSerializer,
                             CompanyCreateSerializer,
                             VacancySerializer,
                             FavoriteSerializer,
                             ResponseSerializer, VacancyCreateSerializer, ClientSerializer, CompanySerializer,
                             LogoutSerializer, ClientProfileSerializer, CompanyProfileSerializer, TokenSerializer,
                             )
from database.customViewsets import ModelViewSetWithoutRetrieve
from database.models import Response as ResponseModel, Favorite
from database.models import Vacancy
from user_auth.models import CustomUser, Client, Company


class ClientPermission(permissions.BasePermission):
    """Class providing permissions to administrators"""

    message = 'You are not a client'

    # request.user.is_authenticated and
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 1:
            return True

        return False


class ClientCreateView(generics.GenericAPIView):
    serializer_class = ClientCreateSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            client = serializer.save()
            refresh = RefreshToken.for_user(client)

            return Response({
                'id': CustomUser.objects.get(email=client.email).id,
                'first_name': CustomUser.objects.get(email=client.email).first_name,
                'last_name': CustomUser.objects.get(email=client.email).last_name,
                'email': client.email,
                'city': client.city_id,
                'phone': client.phone,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientLoginView(CreateAPIView):
    """Class providing user login"""
    serializer_class = ClientLoginSerializer

    def post(self, request, *args, **kwargs):
        """Method providing user login"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if authenticate(email=user['email'], password=user['password']):
            user = CustomUser.objects.get(email=user['email'])
            token = RefreshToken.for_user(user)
            return Response({
                'id': user.id,
                'email': CustomUser.objects.get(email=user.email).email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'refresh_token': str(token),
                'access_token': str(token.access_token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# COMPANY VIEWS ?????????????????????????????
class CompanyPermission(permissions.BasePermission):
    """Class providing permissions to administrators"""

    message = 'You are not a Company'

    # request.user.is_authenticated and
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.user_type == 2:
            return True

        return False


class CompanyCreateView(generics.GenericAPIView):
    serializer_class = CompanyCreateSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            company = serializer.save()
            refresh = RefreshToken.for_user(company)

            return Response({
                'id': CustomUser.objects.get(email=company.email).id,
                'company_name': company.company_name,
                'email': company.email,
                'city': company.city_id,
                'company_description': company.company_description,
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyLoginView(CreateAPIView):
    """Class providing user login"""
    serializer_class = CompanyLoginSerializer

    def post(self, request, *args, **kwargs):
        """Method providing user login"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        if authenticate(email=user['email'], password=user['password']):
            user = CustomUser.objects.get(email=user['email'])
            token = RefreshToken.for_user(user)
            return Response({'id': user.id,
                             'email': CustomUser.objects.get(email=user.email).email,
                             'company_name': user.company.company_name,
                             'company_description': user.company.company_description,
                             'refresh_token': str(token),
                             'access_token': str(token.access_token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Vacancy Views
class VacancyCreateView(ModelViewSetWithoutRetrieve):
    serializer_class = VacancyCreateSerializer
    permission_classes = [CompanyPermission]

    def create(self, request, *args, **kwargs):
        request.data['company'] = request.user
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Vacancy.objects.filter(company=self.request.user)


class VacancySearchView(ListAPIView):
    serializer_class = VacancySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        return queryset


class VacancyListView(ListAPIView):
    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    filterset_class = VacancyFilter


class VacancyDetailView(RetrieveAPIView):
    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()


class FavoriteAddView(APIView):
    permission_classes = [ClientPermission]

    # serializer_class = FavoriteSerializer

    def post(self, request, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return Response({'error': 'Vacancy does not exist'}, status=status.HTTP_404_NOT_FOUND)

        favorite = Favorite(vacancy=vacancy, client_id=request.user.id)
        favorite.save()

        return Response({'success': 'Vacancy added to favorites'}, status=status.HTTP_201_CREATED)

    # def post(self, request, *args, **kwargs):
    #     user = request.user
    #     request.data['client'] = user.id
    #     return super().post(request, *args, **kwargs)


class ResponseAddView(APIView):
    permission_classes = [ClientPermission]
    serializer_class = ResponseSerializer

    def post(self, request, pk):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
        except Vacancy.DoesNotExist:
            return Response({'error': 'Vacancy does not exist'}, status=status.HTTP_404_NOT_FOUND)

        response = ResponseModel(vacancy=vacancy, client_id=request.user.id,
                                 response_text=request.data['response_text'])
        response.save()

        return Response({'success': 'Vacancy added to responses'}, status=status.HTTP_201_CREATED)


class ResponseListView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [ClientPermission]

    def get_queryset(self):
        return ResponseModel.objects.filter(client=self.request.user.id)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ClientProfileView(generics.RetrieveUpdateAPIView, ListCreateAPIView):
    serializer_class = ClientProfileSerializer
    permission_classes = [ClientPermission]

    # get the current user
    def get_object(self):
        return self.request.user


class CompanyProfileView(generics.RetrieveUpdateAPIView, ListCreateAPIView):
    serializer_class = CompanyProfileSerializer
    permission_classes = [CompanyPermission]

    def get_queryset(self):
        return Company.objects.filter(id=self.kwargs['pk'])


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [ClientPermission]

    def get_queryset(self):
        return Favorite.objects.filter(client=self.request.user.id)


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=False)
    def me(self, request):
        if isinstance(self.request.user.id, int) is False:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Client.objects.filter(id=self.request.user.id).prefetch_related('client').first()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(detail=False)
    def me(self, request):
        if isinstance(self.request.user.id, int) is False:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = Company.objects.filter(id=self.request.user.id).first()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VacancyIDView(ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        ids = self.request.query_params.getlist('id_in')
        return Vacancy.objects.filter(id__in=ids)
