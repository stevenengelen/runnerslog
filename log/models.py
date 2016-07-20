from django.db import models

# Create your models here.
class Training(models.Model) :
    distance = models.FloatField()
    executed_time = models.DateTimeField()
    in_zone = models.TimeField()
    average_heart_rate = models.IntegerField()
