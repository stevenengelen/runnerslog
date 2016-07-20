from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Training
from django.core.urlresolvers import resolve
from datetime import time

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
        training.executed_time = '00:12:05'
        training.in_zone = '00:10:58'
        training.average_heart_rate = 152
        training.save()

        saved_training = Training.objects.all()

        self.assertEqual(saved_training.count(), 1)
        self.assertEqual(saved_training[0].distance, 2.3)
        self.assertEqual(saved_training[0].executed_time, time(0, 12, 5))
        self.assertEqual(saved_training[0].in_zone, time(0, 10, 58))
        self.assertEqual(saved_training[0].average_heart_rate, 152)

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
        self.assertEqual(saved_training[0].executed_time, time(0, 12, 5))
        self.assertEqual(saved_training[0].in_zone, time(0, 10, 58))
        self.assertEqual(saved_training[0].average_heart_rate, 152)
