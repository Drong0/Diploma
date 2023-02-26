from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, generics
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import (ClientLoginSerializer,
                             ClientCreateSerializer,
                             CompanyLoginSerializer,
                             CompanyCreateSerializer,
                             VacancySerializer,
                             FavoriteSerializer,
                             ResponseSerializer,
                             ProfileSerializer, VacancyCreateSerializer
                             )
from database.models import Response as ResponseModel
from database.models import Vacancy
from user_auth.models import CustomUser, Client


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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            return Response({'refresh_token': str(token),
                             'access_token': str(token.access_token),
                             'user_type': user.user_type}, status=status.HTTP_200_OK)
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            return Response({'refresh_token': str(token),
                             'access_token': str(token.access_token),
                             'user_type': user.user_type}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Vacancy Views
class VacancyCreateView(CreateAPIView):
    serializer_class = VacancyCreateSerializer
    permission_classes = [CompanyPermission]

    # def post(self, request, *args, **kwargs):
    #     request.data['company'] = request.user.id
    #     return super().post(request, *args, **kwargs)

class VacancyListView(ListAPIView):
    serializer_class = VacancySerializer
    queryset = Vacancy.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'occupation', 'city', 'salary_min', 'salary_max', 'specialization' )


class VacancyDetailView(ListAPIView):
    serializer_class = VacancySerializer

    def get_queryset(self):
        return Vacancy.objects.filter(id=self.kwargs['pk'])


class FavoriteAddView(CreateAPIView):
    permission_classes = [ClientPermission]
    serializer_class = FavoriteSerializer

    def post(self, request, *args, **kwargs):
        request.data['client'] = request.user.id
        request.data['vacancy'] = self.kwargs['pk']
        return super().post(request, *args, **kwargs)


class ResponseAddView(CreateAPIView):
    permission_classes = [ClientPermission]
    serializer_class = ResponseSerializer

    def post(self, request, *args, **kwargs):
        request.data['client'] = request.user.id
        request.data['vacancy'] = self.kwargs['pk']
        return super().post(request, *args, **kwargs)


class ResponseListView(generics.ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [ClientPermission]

    def get_queryset(self):
        return ResponseModel.objects.filter(client=self.request.user.id)


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView, ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [ClientPermission]

    def get_queryset(self):
        return Client.objects.filter(id=self.kwargs['pk'])
