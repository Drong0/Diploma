from django.contrib import admin

from database.models import Vacancy
from user_auth.models import Client, Company
# Register your models here.


admin.site.register(Client)
admin.site.register(Company)
admin.site.register(Vacancy)