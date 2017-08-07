from django.db import models
from datetime import timedelta
from datetime import datetime
# Create your models here.

class TrainingType(models.Model) :
    zone = models.IntegerField(verbose_name = 'Zone: ', help_text = '1', unique = True)
    upper_heart_rate = models.IntegerField(verbose_name = 'Upper heart rate: ', help_text = '145', null = True)
    lower_heart_rate = models.IntegerField(verbose_name = 'Lower heart rate: ', help_text = '155', null = True)
    description = models.CharField(null = True, verbose_name = 'Description: ', max_length = 255)

    @property
    def full_type_as_string(self) :
        ''' return a string with the full description of the training type e.g. Zone 1: 145 - 155 HR '''
        return 'Zone ' + str(self.zone) + ': ' + str(self.lower_heart_rate) + ' - ' + str(self.upper_heart_rate)

class Training(models.Model) :
    # TODO add a date column and add the logic that is the date is not provided,
    # we will use the default date now() (fat models and thin views)
    date = models.DateField(verbose_name = 'Date: ', help_text = 'dd/mm/yyyy', null =True)
    distance = models.FloatField(verbose_name = "Distance: ")
    executed_time = models.DurationField(verbose_name = "Executed time: ", help_text = "HH:MM:SS")
    in_zone = models.DurationField(verbose_name = "In zone: ", help_text = "HH:MM:SS")
    average_heart_rate = models.IntegerField(verbose_name = "Average heart rate: ")
    planned_duration = models.DurationField(verbose_name = "Planned duration: ", help_text ="HH:MM", null = True)
    planned_type_of_training = models.ForeignKey(TrainingType, null = True)
    notes = models.CharField(max_length = 70, verbose_name = "Notes: ", null = True)

    @property
    def date_(self) :
        year = str(self.date.year)
        month = str(self.date.month)
        day = str(self.date.day)

        # make sure we have the right format dd/mm/yyyy
        if len(year) == 2 :
            year = '20' + year
        if len(month) == 1 :
            month = '0' + month
        if len(day) == 1 :
            day = '0' + day
        return day + '/' + month + '/' + year

    @property
    def executed_time_(self) :
        return self.executed_time

    @property
    def in_zone_(self) :
        return self.in_zone

    @property
    def planned_duration_(self) :
        return self.planned_duration

    @property
    def planned_type_of_training_(self) :
        return self.planned_type_of_training.full_type_as_string

    @date_.setter
    def date_(self, value) :
        if '-' in value :
            [y, d, m] = value.split('-')
        else :
            [d, m, y] = value.split('/')
        self.date = datetime(int(y), int(m), int(d))

    @executed_time_.setter
    def executed_time_(self, value) :
        # padding up, so we hve a hh:mm:ss format
        while value.count(':') < 2 :
            value = '00:' + value
        [h, m, s] = value.split(':')
        self.executed_time =  timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    @in_zone_.setter
    def in_zone_(self, value) :
        # padding up, so we hve a hh:mm:yy:ss format
        while value.count(':') < 2 :
            value = '00:' + value
        [h, m, s] = value.split(':')
        self.in_zone = timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    @planned_duration_.setter
    def planned_duration_(self, value) :
        # padding up, so we hve a hh:mm format
        while value.count(':') < 1 :
            value = '00:' + value
        [h, m] = value.split(':')
        self.planned_duration =  timedelta(hours = int(h), minutes = int(m))

    @planned_type_of_training_.setter
    def planned_type_of_training_(self, value) :
        training_type = TrainingType.objects.filter(zone = value)
        # if not training typ is empty
        self.planned_type_of_training = training_type[0]
