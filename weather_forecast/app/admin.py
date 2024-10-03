from django.contrib import admin
from .models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "city1", "city2")

admin.site.register(City, CityAdmin)
    

# Register your models here.
