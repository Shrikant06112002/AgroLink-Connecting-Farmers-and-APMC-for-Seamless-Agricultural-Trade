from django.db import models

# Create your models here.
class Table(models.Model):
    email = models.EmailField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    crop_name = models.CharField(max_length=100)
    seed_type  = models.CharField(max_length=100)
    quality = models.CharField(max_length=25)
    quantity = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()

