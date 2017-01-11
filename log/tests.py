from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Training
from django.core.urlresolvers import resolve
from datetime import timedelta


def make_and_save_training_object(self, distance, executed_time, in_zone, average_heart_rate) :
    training = Training()
    training.distance = distance
    training.executed_time_ = executed_time
    training.in_zone_ = in_zone
    training.average_heart_rate = average_heart_rate
    training.save()

    return training

def assert_saved_training(self, number_of_objects, distance, executed_time, in_zone, average_heart_rate) :
    saved_training = Training.objects.all()

    (hours_et, minutes_et, seconds_et) = executed_time.split(':')
    (hours_iz, minutes_iz, seconds_iz) = in_zone.split(':')
    training = Training.objects.filter(
            distance = distance, 
            executed_time = timedelta(hours = int(hours_et), minutes = int(minutes_et), seconds = int(seconds_et)),
            in_zone = timedelta(hours = int(hours_iz), minutes = int(minutes_iz), seconds = int(seconds_iz)),
            average_heart_rate = average_heart_rate)
    self.assertEqual(saved_training.count(), number_of_objects)
    self.assertIsNotNone(training)

# Create your tests here.
class HomepageTest(TestCase) :
    def test_render_correct_homepage(self) :
        request = HttpRequest()
        response = home_page(request)
        rendered_html = render_to_string('home.html')
        # TODO : get rid of this csrf thing for once and for all!
        # self.assertEqual(response.content.decode(), rendered_html)

    def test_root_url_resolves_to_home_page_view(self) :
        found = resolve('/')
        self.assertEqual(found.func, home_page)

class TrainingDataModelTest(TestCase) :
    def setUp(self) :
        self.distance = 2.3
        self.executed_time = '00:12:05'
        self.in_zone = '00:10:58'
        self.average_heart_rate = 152
        
        self.second_distance = 12.3
        self.second_executed_time = '01:12:05'
        self.second_in_zone = '01:10:58'
        self.second_average_heart_rate = 148

    def test_store_and_retrieve_training_data(self) :
        make_and_save_training_object(self, self.distance, self.executed_time, self.in_zone, self.average_heart_rate)
        assert_saved_training(self, 1, self.distance, self.executed_time, self.in_zone, self.average_heart_rate)

        make_and_save_training_object(self, self.second_distance, self.second_executed_time, self.second_in_zone, self.second_average_heart_rate)
        assert_saved_training(self, 2, self.second_distance, self.second_executed_time, self.second_in_zone, self.second_average_heart_rate)

class NewTrainingDataTest(TestCase) :
    def setUp(self) :
        self.distance = 2.3
        self.executed_time = '00:12:05'
        self.in_zone = '00:10:58'
        self.average_heart_rate = 152
        
        self.second_distance = 12.3
        self.second_executed_time = '01:12:05'
        self.second_in_zone = '01:10:58'
        self.second_average_heart_rate = 148

    def test_saves_a_POST_request(self) :
        self.client.post('/', data = {
            'distance' : self.distance,
            'executed_time' : self.executed_time,
            'in_zone' : self.in_zone,
            'average_heart_rate' : self.average_heart_rate,
            })
        assert_saved_training(self, 1, self.distance, self.executed_time, self.in_zone, self.average_heart_rate)

    def test_saves_a_second_POST_request(self) :
        self.client.post('/', data = {
            'distance' : self.distance,
            'executed_time' : self.executed_time,
            'in_zone' : self.in_zone,
            'average_heart_rate' : self.average_heart_rate,
            })
        assert_saved_training(self, 1, self.distance, self.executed_time, self.in_zone, self.average_heart_rate)

        self.client.post('/', data = {
            'distance' : self.second_distance,
            'executed_time' : self.second_executed_time,
            'in_zone' : self.second_in_zone,
            'average_heart_rate' : self.second_average_heart_rate,
            })

        assert_saved_training(self, 2, self.second_distance, self.second_executed_time, self.second_in_zone, self.second_average_heart_rate)


    def test_reads_from_database_when_opening_home_page(self) :
        # first we save some data using a POST
        self.client.post('/', data = {
            'distance' : self.distance,
            'executed_time' : self.executed_time,
            'in_zone' : self.in_zone,
            'average_heart_rate' : self.average_heart_rate,
            })

        # next we launch a new http request and check if the data saved is in the response
        request = HttpRequest()
        response = home_page(request)
        response_text = response.content.decode('ascii')

        # find the occurences of <tr>, substract 1 from the <th> row, and that must be equal to the number of Training.objects.all()
        number_of_saved_trainings = Training.objects.all().count()
        number_of_rows_in_table = response_text.count('<tr>') - 1

        self.assertEqual(number_of_saved_trainings, 1)
        self.assertEqual(number_of_rows_in_table, 1)
