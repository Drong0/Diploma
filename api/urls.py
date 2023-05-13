from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import VacancyIDView

router = DefaultRouter()

router.register("clients", views.ClientViewSet)
router.register("companies", views.CompanyViewSet)
router.register("vacancy", views.VacancyCreateView, basename="vacancy")
router.register("skill", views.SkillView, basename="skill")
router.register("occupation", views.OccupationView, basename="occupation")
router.register("specialization", views.SpecializationView, basename="specialization")
router.register("companyResponse", views.CompanyResponseView, basename="companyResponse")
urlpatterns = router.urls
urlpatterns += [
    path('client/register/', views.ClientCreateView.as_view(), name='register'),
    path('client/login/', views.ClientLoginView.as_view(), name='login'),

    path('company/register/', views.CompanyCreateView.as_view(), name='register'),
    path('company/login/', views.CompanyLoginView.as_view(), name='login'),

    path('allVacancy/', views.VacancyListView.as_view(), name='vacancies'),
    path('vacancyByID/<int:pk>', views.VacancyDetailView.as_view(), name='vacancies'),
    path('like/<int:pk>', views.FavoriteAddView.as_view(), name='like'),
    path('responseAdd/<int:pk>/', views.ResponseAddView.as_view(), name='response'),
    path('like/list/', views.FavoriteListView.as_view(), name='favorite'),
    path('myResponse/list/', views.ResponseListView.as_view(), name='response'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('vacancyIDs/', VacancyIDView.as_view()),
    path('vacancySearch/', views.VacancySearchView.as_view(), name='search'),
    path('responseByVacancy/<int:pk>/', views.ResponseByVacancyView.as_view(), name='response'),
    path('responseByIdUpdate/<int:pk>/', views.ResponseUpdateView.as_view(), name='response'),
    path('like/<int:pk>/', views.FavoriteDeleteView.as_view(), name='favorite'),
]