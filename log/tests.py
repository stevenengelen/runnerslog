from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Training
from django.core.urlresolvers import resolve
from datetime import timedelta

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
        training = Training()
        training.distance = 2.3
        training.executed_time_ = '00:12:05'
        training.in_zone_ = '00:10:58'
        training.average_heart_rate = 152
        training.save()

        saved_training = Training.objects.all()

        self.assertEqual(saved_training.count(), 1)
        self.assertEqual(saved_training[0].distance, 2.3)
        self.assertEqual(saved_training[0].executed_time_, timedelta(hours = 0, minutes = 12, seconds = 5))
        self.assertEqual(saved_training[0].in_zone_, timedelta(hours = 0, minutes = 10, seconds = 58))
        self.assertEqual(saved_training[0].average_heart_rate, 152)
        
        second_training = Training()
        second_training.distance = 12.3
        second_training.executed_time_ = '01:12:05'
        second_training.in_zone_ = '01:10:58'
        second_training.average_heart_rate = 148
        second_training.save()

        saved_trainings = Training.objects.all()

        self.assertEqual(saved_trainings.count(), 2)
        self.assertEqual(saved_trainings[1].distance, 12.3)
        self.assertEqual(saved_trainings[1].executed_time_, timedelta(hours =1, minutes = 12, seconds = 5))
        self.assertEqual(saved_trainings[1].in_zone_, timedelta(hours = 1, minutes = 10, seconds = 58))
        self.assertEqual(saved_trainings[1].average_heart_rate, 148)

class NewTrainingDataTest(TestCase) :
    def test_saves_a_POST_request(self) :
        self.client.post('/', data = {
            'item_distance' : '2.3',
            'item_executed_time' : '00:12:05',
            'item_in_zone' : '00:10:58',
            'item_average_heart_rate' : '152',
            })

        saved_training = Training.objects.all()

        self.assertEqual(saved_training.count(), 1)
        self.assertEqual(saved_training[0].distance, 2.3)
        self.assertEqual(saved_training[0].executed_time_, timedelta(hours = 0, minutes = 12, seconds = 5))
        self.assertEqual(saved_training[0].in_zone_, timedelta(hours = 0, minutes = 10, seconds = 58))
        self.assertEqual(saved_training[0].average_heart_rate, 152)

    def test_saves_a_second_POST_request(self) :
        self.client.post('/', data = {
            'item_distance' : '2.3',
            'item_executed_time' : '00:12:05',
            'item_in_zone' : '00:10:58',
            'item_average_heart_rate' : '152',
            })

        self.client.post('/', data = {
            'item_distance' : '12.3',
            'item_executed_time' : '01:12:05',
            'item_in_zone' : '01:10:58',
            'item_average_heart_rate' : '142',
            })

        saved_training = Training.objects.all()

        self.assertEqual(saved_training.count(), 2)
        self.assertEqual(saved_training[0].distance, 2.3)
        self.assertEqual(saved_training[0].executed_time_, timedelta(hours = 0, minutes = 12, seconds = 5))
        self.assertEqual(saved_training[0].in_zone_, timedelta(hours = 0, minutes = 10, seconds = 58))
        self.assertEqual(saved_training[0].average_heart_rate, 152)

        self.assertEqual(saved_training[1].distance, 12.3)
        self.assertEqual(saved_training[1].executed_time_, timedelta(hours = 1, minutes = 12, seconds = 5))
        self.assertEqual(saved_training[1].in_zone_, timedelta(hours = 1, minutes = 10, seconds = 58))
        self.assertEqual(saved_training[1].average_heart_rate, 142)
