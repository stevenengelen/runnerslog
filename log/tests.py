from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Training
from django.core.urlresolvers import resolve
from datetime import timedelta
from datetime import datetime
import log.testdata


def make_and_save_training_object(self, data) :
    ''' data is a dictionary with the values of a training session '''
    training = Training()
    training.date_ = data['date']
    training.distance = data['distance']
    training.average_heart_rate = data['average_heart_rate']
    training.planned_type_of_training = data['planned_type_of_training']
    training.executed_time_ = data['executed_time']
    training.in_zone_ = data['in_zone']
    training.planned_duration_ = data['planned_duration']
    training.save()

    return training

def assert_saved_training(self, number_of_objects, data) :
    ''' checks if training session has been saved - data is a dictionary conatining the session to compare to '''
    saved_training = Training.objects.all()

    # padding up, so we hve a hh:mm:yy:ss format
    while data['executed_time'].count(':') < 2 :
        data['executed_time'] = '00:' + data['executed_time']
    (hours_et, minutes_et, seconds_et) = data['executed_time'].split(':')
    # padding up, so we hve a hh:mm:yy:ss format
    while data['in_zone'].count(':') < 2 :
        data['in_zone'] = '00:' + data['in_zone']
    (hours_iz, minutes_iz, seconds_iz) = data['in_zone'].split(':')
    (day, month, year) = data['date'].split('/')
    
    training = Training.objects.filter(
            date = datetime(int(year), int(month), int(day)),
            distance = data['distance'], 
            average_heart_rate = data['average_heart_rate'],
            planned_type_of_training = data['planned_type_of_training'],
            executed_time = timedelta(hours = int(hours_et), minutes = int(minutes_et), seconds = int(seconds_et)),
            in_zone = timedelta(hours = int(hours_iz), minutes = int(minutes_iz), seconds = int(seconds_iz)),
            planned_duration = data['planned_duration']
            )
            
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
        make_and_save_training_object(self, log.testdata.FIRST_TRAINING_SESSION)
        assert_saved_training(self, 1, log.testdata.FIRST_TRAINING_SESSION)

        make_and_save_training_object(self, log.testdata.SECOND_TRAINING_SESSION)
        assert_saved_training(self, 2, log.testdata.SECOND_TRAINING_SESSION)

class NewTrainingDataTest(TestCase) :
    def test_saves_a_POST_request(self) :
        self.client.post('/', log.testdata.FIRST_TRAINING_SESSION)
        assert_saved_training(self, 1, log.testdata.FIRST_TRAINING_SESSION)

    def test_saves_a_second_POST_request(self) :
        self.client.post('/', log.testdata.FIRST_TRAINING_SESSION)
        assert_saved_training(self, 1, log.testdata.FIRST_TRAINING_SESSION)

        self.client.post('/', log.testdata.SECOND_TRAINING_SESSION)
        assert_saved_training(self, 2, log.testdata.FIRST_TRAINING_SESSION)
        assert_saved_training(self, 2, log.testdata.SECOND_TRAINING_SESSION)

    def test_reads_from_database_when_opening_home_page(self) :
        # first we save some data using a POST
        self.client.post('/', log.testdata.FIRST_TRAINING_SESSION)

        # next we launch a new http request and check if the data saved is in the response
        request = HttpRequest()
        response = home_page(request)
        response_text = response.content.decode('ascii')

        # find the occurences of <tr>, substract 1 from the <th> row, and that must be equal to the number of Training.objects.all()
        number_of_saved_trainings = Training.objects.all().count()
        number_of_rows_in_table = response_text.count('<tr>') - 1

        self.assertEqual(number_of_saved_trainings, 1)
        self.assertEqual(number_of_rows_in_table, 1)

        # check if the data is present
        data = log.testdata.FIRST_TRAINING_SESSION.values()
        for element in data :
            self.assertTrue(element in response_text, element + ' not in rendered html ')
