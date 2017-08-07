from log.models import TrainingType

FIRST_TYPE_OF_TRAINING = { 'zone' : 1, 'upper_heart_rate' : 155, 'lower_heart_rate' : 145, 'description' : 'Dit is de lange duurloop zone.' }
SECOND_TYPE_OF_TRAINING = { 'zone' : 2, 'upper_heart_rate' : 185, 'lower_heart_rate' : 175, 'description' : 'Dit is de intensieve duurloop zone.' }

FIRST_TRAINING = { 'date' : '07/02/2017', 'distance' : '15', 'average_heart_rate' : '149', 'planned_type_of_training' : '1',  'executed_time' : '1:32:15', 'in_zone' : '1:18:27', 'planned_duration' : '2:00', 'notes' : 'Slight aching knee' }
SECOND_TRAINING = { 'date' : '03/02/2017', 'distance' : '9.9', 'average_heart_rate' : '172', 'planned_type_of_training' : '2', 'executed_time' : '52:45', 'in_zone' : '7:24', 'planned_duration' : '45', 'notes' : 'Lot\'s of wind and snow' }


def insert_first_type_of_training() :
    first_type_of_training = TrainingType()
    first_type_of_training.zone = FIRST_TYPE_OF_TRAINING['zone']
    first_type_of_training.lower_heart_rate = FIRST_TYPE_OF_TRAINING['lower_heart_rate']
    first_type_of_training.upper_heart_rate = FIRST_TYPE_OF_TRAINING['upper_heart_rate']
    first_type_of_training.description = FIRST_TYPE_OF_TRAINING['description']
    first_type_of_training.save()

def insert_second_type_of_training() :
    second_type_of_training = TrainingType()
    second_type_of_training.zone = SECOND_TYPE_OF_TRAINING['zone']
    second_type_of_training.lower_heart_rate = SECOND_TYPE_OF_TRAINING['lower_heart_rate']
    second_type_of_training.upper_heart_rate = SECOND_TYPE_OF_TRAINING['upper_heart_rate']
    second_type_of_training.description = SECOND_TYPE_OF_TRAINING['description']
    second_type_of_training.save()

def get_first_training_session() :
    insert_first_type_of_training()
    return FIRST_TRAINING

def get_second_training_session() :
    ''' delivers data as input for html '''
    insert_second_type_of_training()
    return SECOND_TRAINING

def get_first_training_session_in_text_form() :
    ''' delivers data as input for the webpage '''
    first_training_session = get_first_training_session().copy()
    # first we put the string in a local copy of the data dictionary instead of the index, since it is the string that is displayed on the page
    training_types = TrainingType.objects.filter(zone = first_training_session['planned_type_of_training'])
    first_training_session['planned_type_of_training'] = training_types[0].full_type_as_string
    return first_training_session

def get_second_training_session_in_text_form() :
    ''' delivers data as input for the webpage '''
    second_training_session = get_second_training_session().copy()
    # first we put the string in a local copy of the data dictionary instead of the index, since it is the string that is displayed on the page
    training_types = TrainingType.objects.filter(zone = second_training_session['planned_type_of_training'])
    second_training_session['planned_type_of_training'] = training_types[0].full_type_as_string
    return second_training_session
