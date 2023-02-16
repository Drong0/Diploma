from django.urls import path

from . import views

# Create your urls here.

urlpatterns = [
    path('client/register/', views.ClientCreateView.as_view(), name='register'),
    path('client/login/', views.ClientLoginView.as_view(), name='login'),

    path('company/register/', views.CompanyCreateView.as_view(), name='register'),
    path('company/login/', views.CompanyLoginView.as_view(), name='login'),

    path('vacancy/create/', views.VacancyCreateView.as_view(), name='vacancies'),
    path('vacancy/list/', views.VacancyListView.as_view(), name='vacancies'),
    path('vacancy/<int:pk>', views.VacancyDetailView.as_view(), name='vacancies'),
    path('vacancy/<int:pk>/like/', views.FavoriteAddView.as_view(), name='like'),
    path('vacancy/<int:pk>/response/', views.ResponseAddView.as_view(), name='response'),
    path('vacancy/response/list/', views.ResponseListView.as_view(), name='response'),
]
