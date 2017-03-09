from log.models import TrainingType

FIRST_TYPE_OF_TRAINING = { 'zone' : 1, 'upper_heart_rate' : 155, 'lower_heart_rate' : 145, 'description' : 'Dit is de lange duurloop zone.' }
SECOND_TYPE_OF_TRAINING = { 'zone' : 2, 'upper_heart_rate' : 185, 'lower_heart_rate' : 175, 'description' : 'Dit is de intensieve duurloop zone.' }

# TODO : do something to fill in the right type of training

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

'''
def get_first_training_session_data() :
    ''' '''delivers data for the database ''' '''
    insert_first_type_of_training()
    training_types_zone_one = TrainingType.objects.filter(zone = 1)
    return { 'date' : '07/02/2017', 'distance' : '15', 'average_heart_rate' : '149', 'planned_type_of_training' : training_types_zone_one[0], 'executed_time' : '1:32:15', 'in_zone' : '1:18:27', 'planned_duration' : '2:00', 'notes' : 'Slight aching knee' }

def get_second_training_session_data() :
    ''' ''' delivers data for the database ''' '''
    insert_second_type_of_training()
    training_types_zone_two = TrainingType.objects.filter(zone = 2)
    return { 'date' : '03/02/2017', 'distance' : '9.9', 'average_heart_rate' : '172', 'planned_type_of_training' : training_types_zone_two[0], 'executed_time' : '52:45', 'in_zone' : '7:24', 'planned_duration' : '45', 'notes' : 'Lot\'s of wind and snow' }
'''
def get_first_training_session() :
    ''' delivers data as input for html '''
    insert_first_type_of_training()
    return { 'date' : '07/02/2017', 'distance' : '15', 'average_heart_rate' : '149', 'planned_type_of_training' : '1',  'executed_time' : '1:32:15', 'in_zone' : '1:18:27', 'planned_duration' : '2:00', 'notes' : 'Slight aching knee' }

def get_second_training_session() :
    ''' delivers data as input for html '''
    insert_second_type_of_training()
    return { 'date' : '03/02/2017', 'distance' : '9.9', 'average_heart_rate' : '172', 'planned_type_of_training' : '2', 'executed_time' : '52:45', 'in_zone' : '7:24', 'planned_duration' : '45', 'notes' : 'Lot\'s of wind and snow' }
