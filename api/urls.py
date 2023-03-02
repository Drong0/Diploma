from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("client", views.ClientViewSet)
router.register("company", views.CompanyViewSet)
urlpatterns = router.urls
urlpatterns += [
    path('client/register/', views.ClientCreateView.as_view(), name='register'),
    path('client/login/', views.ClientLoginView.as_view(), name='login'),

    path('company/register/', views.CompanyCreateView.as_view(), name='register'),
    path('company/login/', views.CompanyLoginView.as_view(), name='login'),

    path('vacancy/create/', views.VacancyCreateView.as_view(), name='vacancies'),
    path('vacancy/list/', views.VacancyListView.as_view(), name='vacancies'),
    path('vacancy/<int:pk>', views.VacancyDetailView.as_view(), name='vacancies'),
    path('vacancy/<int:pk>/like/', views.FavoriteAddView.as_view(), name='like'),
    path('vacancy/<int:pk>/response/', views.ResponseAddView.as_view(), name='response'),
    path('user/favorite/list/', views.FavoriteListView.as_view(), name='favorite'),
    path('vacancy/response/list/', views.ResponseListView.as_view(), name='response'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]