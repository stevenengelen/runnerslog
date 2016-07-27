from django.db import models
from datetime import timedelta

# Create your models here.
class Training(models.Model) :
    distance = models.FloatField()
    executed_time = models.DurationField()
    in_zone = models.DurationField()
    average_heart_rate = models.IntegerField()

    @property
    def executed_time_(self) :
        return self.executed_time

    @property
    def in_zone_(self) :
        return self.in_zone

    @executed_time_.setter
    def executed_time_(self, value) :
        [h, m, s] = value.split(':')
        self.executed_time =  timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    @in_zone_.setter
    def in_zone_(self, value) :
        [h, m, s] = value.split(':')
        self.in_zone = timedelta(hours = int(h), minutes = int(m), seconds = int(s))
