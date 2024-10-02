from django.contrib import admin
from .models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ('city1', 'city2')

admin.site.register(City, CityAdmin)