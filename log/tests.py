from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Training
from django.core.urlresolvers import resolve
from datetime import timedelta
from datetime import datetime
import log.testdata
from .models import TrainingType

def make_and_save_training_object(self, data) :
    ''' data is a dictionary with the values of a training session '''
    training = Training()
    training.date_ = data['date']
    training.distance = data['distance']
    training.average_heart_rate = data['average_heart_rate']
    training.planned_type_of_training_ = data['planned_type_of_training']
    training.executed_time_ = data['executed_time']
    training.in_zone_ = data['in_zone']
    training.planned_duration_ = data['planned_duration']
    training.notes = data['notes']
    training.save()

    return training

def assert_saved_training(self, number_of_objects, data) :
    ''' checks if training session has been saved - data is a dictionary containing the session to compare to '''
    saved_training = Training.objects.all()

    # padding up, so we have a hh:mm:ss format
    while data['executed_time'].count(':') < 2 :
        data['executed_time'] = '00:' + data['executed_time']
    (hours_et, minutes_et, seconds_et) = data['executed_time'].split(':')
    # padding up, so we have a hh:mm:ss format
    while data['in_zone'].count(':') < 2 :
        data['in_zone'] = '00:' + data['in_zone']
    (hours_iz, minutes_iz, seconds_iz) = data['in_zone'].split(':')
    (day, month, year) = data['date'].split('/')
    # padding up, so we have a hh:mm format
    while data['planned_duration'].count(':') < 1 :
        data['planned_duration'] = '00:' + data['planned_duration']
    (planned_hours, planned_minutes) = data['planned_duration'].split(':')
    training_types = TrainingType.objects.filter(zone = data['planned_type_of_training'])
    self.assertIsNotNone(training_types)
    the_planned_type_of_training = training_types[0]

    training = Training.objects.filter(
            date = datetime(int(year), int(month), int(day)),
            distance = data['distance'], 
            average_heart_rate = data['average_heart_rate'],
            planned_type_of_training = the_planned_type_of_training,
            executed_time = timedelta(hours = int(hours_et), minutes = int(minutes_et), seconds = int(seconds_et)),
            in_zone = timedelta(hours = int(hours_iz), minutes = int(minutes_iz), seconds = int(seconds_iz)),
            planned_duration = timedelta(hours = int(planned_hours), minutes = int(planned_minutes)),
            notes = data['notes']
            )
            
    self.assertEqual(saved_training.count(), number_of_objects)
    self.assertIsNotNone(training[0])
    # check if the saved training sessions has one (and only one) training type, and the right training type
    self.assertEqual(training[0].planned_type_of_training, the_planned_type_of_training)

# Create your tests here.
class HomepageTest(TestCase) :
    def test_render_correct_homepage(self) :
        request = HttpRequest()
        response = home_page(request)
        rendered_html = render_to_string('home.html')
        # TODO : get rid of this csrf thing for once and for all!
        print('response')
        print('-------------------------------------------------')
        print(response.content.decode())
        print('renderd_html')
        print('-------------------------------------------------')
        print(rendered_html)
        self.assertEqual(response.content.decode(), rendered_html)

    def test_root_url_resolves_to_home_page_view(self) :
        found = resolve('/')
        self.assertEqual(found.func, home_page)

class TrainingDataModelTest(TestCase) :
    def setUp(self) :
        self.first_training_session = log.testdata.get_first_training_session()
        self.second_training_session = log.testdata.get_second_training_session()

    def test_store_and_retrieve_training_data(self) :
        make_and_save_training_object(self, self.first_training_session)
        assert_saved_training(self, 1, self.first_training_session)

        make_and_save_training_object(self, self.second_training_session)
        assert_saved_training(self, 2, self.second_training_session)

    def test_if_more_than_one_type_of_training_is_present_in_database(self) :
        ''' Type of training is something like \'Zone 1: 145 - 155 HR\' '''

        # we check if there is something in there
        type_of_training = TrainingType.objects.all()
        self.assertGreater(type_of_training.count(), 1, 'there are not enough training types available in the database')

class NewTrainingDataTest(TestCase) :
    def setUp(self) :
        self.first_training_session = log.testdata.get_first_training_session()
        self.second_training_session = log.testdata.get_second_training_session()

    def test_saves_a_POST_request(self) :
        self.client.post('/', self.first_training_session)
        assert_saved_training(self, 1, self.first_training_session)

    def test_saves_a_second_POST_request(self) :
        self.client.post('/', self.first_training_session)
        assert_saved_training(self, 1, self.first_training_session)

        self.client.post('/', self.second_training_session)
        assert_saved_training(self, 2, self.first_training_session)
        assert_saved_training(self, 2, self.second_training_session)

    def test_reads_from_database_when_opening_home_page(self) :
        # first we save some data using a POST
        self.client.post('/', self.first_training_session)

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
        html_data = log.testdata.get_first_training_session_in_text_form()
        data = html_data.values()
        for element in data :
            self.assertTrue(str(element) in response_text, str(element) + ' not in rendered html ')
