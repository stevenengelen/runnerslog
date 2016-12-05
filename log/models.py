from django.db import models
from datetime import timedelta

# Create your models here.
class Training(models.Model) :
    # TODO add a date column and add the logic that is the date is not provided,
    # we will use the default date now() (fat models and thin views)
    distance = models.FloatField(verbose_name = "Distance: ")
    executed_time = models.DurationField(verbose_name = "Executed time: ", help_text = "HH:MM:SS")
    in_zone = models.DurationField(verbose_name = "In zone: ", help_text = "HH:MM:SS")
    average_heart_rate = models.IntegerField(verbose_name = "Average heart rate: ")

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
