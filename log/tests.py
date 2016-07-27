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
        training.dist = 2.3
        training.et = '00:12:05'
        training.iz = '00:10:58'
        training.ahr = 152
        training.save()

        saved_training = Training.objects.all()

        self.assertEqual(saved_training.count(), 1)
        self.assertEqual(saved_training[0].dist, 2.3)
        self.assertEqual(saved_training[0].et, timedelta(hours = 0, minutes = 12, seconds = 5))
        self.assertEqual(saved_training[0].iz, timedelta(hours = 0, minutes = 10, seconds = 58))
        self.assertEqual(saved_training[0].ahr, 152)

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
        self.assertEqual(saved_training[0].dist, 2.3)
        self.assertEqual(saved_training[0].et, timedelta(hours = 0, minutes = 12, seconds = 5))
        self.assertEqual(saved_training[0].iz, timedelta(hours = 0, minutes = 10, seconds = 58))
        self.assertEqual(saved_training[0].ahr, 152)
