from django.db import models
from datetime import timedelta

# Create your models here.
class Training(models.Model) :
    distance = models.FloatField()
    executed_time = models.DurationField()
    in_zone = models.DurationField()
    average_heart_rate = models.IntegerField()

    @property
    def dist(self) :
        return self.distance

    @property
    def et(self) :
        return self.executed_time

    @property
    def iz(self) :
        return self.in_zone

    @property
    def ahr(self) :
        return self.average_heart_rate

    @dist.setter
    def dist(self, value) :
        self.distance = value

    @et.setter
    def et(self, value) :
        [h, m, s] = value.split(':')
        self.executed_time =  timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    @iz.setter
    def iz(self, value) :
        [h, m, s] = value.split(':')
        self.in_zone = timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    @ahr.setter
    def ahr(self, value) :
        self.average_heart_rate = value
