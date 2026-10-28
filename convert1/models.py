from django.db import models

# Create your models here.

class History(models.Model):
    input = models.CharField(max_length=10)
    output = models.CharField(max_length=10)