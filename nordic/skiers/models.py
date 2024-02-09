from django.db import models

# Create your models here.
class Sites(models.Model):
    site = models.CharField(max_length=255)