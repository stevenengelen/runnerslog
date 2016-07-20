from django.shortcuts import render
from .models import Training

# Create your views here.

# TODO: refactor to a class based view
def home_page(request) :
    if request.method == 'POST' :
        training = Training()
        training.distance = request.POST['item_distance']
        training.executed_time = request.POST['item_executed_time']
        training.in_zone = request.POST['item_in_zone']
        training.average_heart_rate = request.POST['item_average_heart_rate']
        training.save()
        
        training = Training.objects.all()

        return render(request, 'home.html', { 'training' : training[0] })

    return render(request, 'home.html')
