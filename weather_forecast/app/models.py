from django.db import models

class City(models.Model):
  city1 = models.CharField(max_length=255)
  city2 = models.CharField(max_length=255, null=True)
