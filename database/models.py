from django.db import models

from user_auth.models import Company, Client, City


# HH
class Occupation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    salary_max = models.IntegerField()
    salary_min = models.IntegerField()
    city = models.ForeignKey(City,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    company = models.ForeignKey(Company,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    is_deleted = models.BooleanField(default=False)

    STATUS = (
        (True, 'Active'),
        (False, 'Inactive')
    )
    status = models.BooleanField(choices=STATUS, default=True)
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, null=True, blank=True)


class Specialization(models.Model):
    name = models.CharField(max_length=255)
    vacancy = models.ManyToManyField(Vacancy, related_name='specializations')


class Skill(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.ManyToManyField(Specialization, related_name='skills')


class Response(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
