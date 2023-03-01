from django_filters.rest_framework import FilterSet, MultipleChoiceFilter

from database.models import Specialization, Occupation, Vacancy


class VacancyFilter(FilterSet):
    specialization = MultipleChoiceFilter(field_name='specialization__name', choices=Specialization.objects.all().values_list('name', 'name'))
    occupation = MultipleChoiceFilter(field_name='occupation__name', choices=Occupation.objects.all().values_list('name', 'name'),)

    class Meta:
        model = Vacancy
        fields = ['name', 'occupation', 'city', 'salary_min', 'salary_max', 'specialization']
