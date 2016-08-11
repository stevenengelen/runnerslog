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
    def test_store_and_retrieve_training_data(self) :
        distance = 2.3
        executed_time = '00:12:05'
        in_zone = '00:10:58'
        average_heart_rate = 152

        make_and_save_training_object(self, distance, executed_time, in_zone, average_heart_rate)
        assert_saved_training(self, 1, distance, executed_time, in_zone, average_heart_rate)
        
        second_training_distance = 12.3
        second_training_executed_time = '01:12:05'
        second_training_in_zone = '01:10:58'
        second_training_average_heart_rate = 148

        make_and_save_training_object(self, second_training_distance, second_training_executed_time, second_training_in_zone, second_training_average_heart_rate)
        assert_saved_training(self, 2, second_training_distance, second_training_executed_time, second_training_in_zone, second_training_average_heart_rate)

class NewTrainingDataTest(TestCase) :
    def test_saves_a_POST_request(self) :
        distance = 2.3
        executed_time = '00:12:05'
        in_zone = '00:10:58'
        average_heart_rate = 152

        self.client.post('/', data = {
            'item_distance' : distance,
            'item_executed_time' : executed_time,
            'item_in_zone' : in_zone,
            'item_average_heart_rate' : average_heart_rate,
            })

        assert_saved_training(self, 1, distance, executed_time, in_zone, average_heart_rate)

    def test_saves_a_second_POST_request(self) :
        distance = 2.3
        executed_time = '00:12:05'
        in_zone = '00:10:58'
        average_heart_rate = 152
        
        self.client.post('/', data = {
            'item_distance' : distance,
            'item_executed_time' : executed_time,
            'item_in_zone' : in_zone,
            'item_average_heart_rate' : average_heart_rate,
            })

        assert_saved_training(self, 1, distance, executed_time, in_zone, average_heart_rate)

        distance = 12.3
        executed_time = '01:12:05'
        in_zone = '01:10:58'
        average_heart_rate = 142
        
        self.client.post('/', data = {
            'item_distance' : distance,
            'item_executed_time' : executed_time,
            'item_in_zone' : in_zone,
            'item_average_heart_rate' : average_heart_rate,
            })

        assert_saved_training(self, 2, distance, executed_time, in_zone, average_heart_rate)

    def test_reads_from_database_when_opening_home_page(self) :
        request = HttpRequest()
        response = home_page(request)
        rendered_html = render_to_string('home.html')

        print(rendered_html)

        # find the occurences of <td>, divide them by 4 to get the number of rows, and that must be equal to the number of Training.objects.all()
        number_of_saved_trainings = Training.objects.all().count()
        number_of_rows_in_table = rendered_html.count('<td>') / 4

        print(number_of_saved_trainings)
        print(number_of_rows_in_table)
        # self.assertEqual(number_of_saved_trainings, 
