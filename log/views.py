from django.shortcuts import render
from .models import Training
from .models import TrainingType

# Create your views here.

# TODO: create a forms.py file, which will contain a form class inheriting from forms.Form
# - validation needs to be done in this class
# TODO: refactor to a class based view
def home_page(request) :
    if request.method == 'POST' :
        training = Training()
        training.date_ = request.POST['date']
        training.distance = request.POST['distance']
        training.executed_time_ = request.POST['executed_time']
        training.in_zone_ = request.POST['in_zone']
        training.average_heart_rate = request.POST['average_heart_rate']
        training.planned_duration_ = request.POST['planned_duration']
        training.planned_type_of_training_ = request.POST['planned_type_of_training']
        training.notes = request.POST['notes']
        training.save()
    
    training = Training.objects.all()
    training_types = TrainingType.objects.all()
    # TODO: why do we give the request to the render?
    return render(request, 'home.html', { 'training_log' : training,
                                          'training_types' : training_types } )
