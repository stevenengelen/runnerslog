from selenium.webdriver import Chrome
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import log.testdata
from log.models import TrainingType

class NewTrainingData(StaticLiveServerTestCase) :
    def setUp(self) :
        self.browser = Chrome()
        self.browser.implicitly_wait(3)
        self.first_training_session = log.testdata.get_first_training_session()
        self.second_training_session = log.testdata.get_second_training_session()

    def tearDown(self) :
        self.browser.quit()

    def user_sees_inputfields_and_enters_data(self, data) :
        '''checks if inputfields are there and enters data in them - data is a dictionary,
        keys are the same as the names used in the html form'''

        
        # user sees that the page is divided in 2 parts, a part for input of a 
        # training session, and a part that displays previous inputted sessions in a
        # table.

        # in the input part, user sees:

        # a date edit box
        date_editbox = self.browser.find_element_by_name('date')
        self.assertIsNotNone(date_editbox)

        # a distance edit box
        distance_editbox = self.browser.find_element_by_name('distance')
        self.assertIsNotNone(distance_editbox)
        
        # an average HR edit box
        average_heart_rate_editbox = self.browser.find_element_by_name('average_heart_rate')
        self.assertIsNotNone(average_heart_rate_editbox)

        # a planned type of training select box
        planned_type_of_training_select = Select(self.browser.find_element_by_name('planned_type_of_training'))
        self.assertIsNotNone(planned_type_of_training_select)

        # an executed time edit box
        executed_time_editbox = self.browser.find_element_by_name('executed_time')
        self.assertIsNotNone(executed_time_editbox)

        # an in zone edit box
        in_zone_editbox = self.browser.find_element_by_name('in_zone')
        self.assertIsNotNone(in_zone_editbox)

        # a planned duration edit box
        planned_duration_editbox = self.browser.find_element_by_name('planned_duration')
        self.assertIsNotNone(planned_duration_editbox)

        # a notes textarea
        notes_textarea = self.browser.find_element_by_name('notes')
        self.assertIsNotNone(notes_textarea)

        # user sees a submit button with the text 'Save' on it
        submit_button = self.browser.find_element_by_id('submit_button')
        self.assertEqual(submit_button.get_attribute('value'), 'Save')

        # user enters data in the 4 fields an presses submit
        # TODO : user sees he gets redirected to the same home url
        date_editbox.send_keys(data['date'])
        distance_editbox.send_keys(data['distance'])
        average_heart_rate_editbox.send_keys(data['average_heart_rate'])
        # TODO we shoud do soething about this, I would like to select by text, since that is more correct than by index
        # planned_type_of_training_select.select_by_visible_text(data['planned_type_of_training'])
        planned_type_of_training_select.select_by_index(int(data['planned_type_of_training']) - 1)
        executed_time_editbox.send_keys(data['executed_time'])
        in_zone_editbox.send_keys(data['in_zone'])
        planned_duration_editbox.send_keys(data['planned_duration'])
        notes_textarea.send_keys(data['notes'])

        submit_button.submit()
        
       
    def check_entered_row_of_data_on_screen(self, row_to_check, data) :
        ''' checks one training session  of data entered - data is a dictionary with keys same as names used in the html form.
            the row to check is 1-based, the array of rows is 0 based. but this is not a problem, since the table_row[0] is the header row,
            and we are not going to check that one. '''
        table_rows = self.browser.find_elements_by_tag_name('tr')
        
        # first we put the string in a local copy of the data dictionary instead of the index, since it is the string that is displayed on the page
        local_data = data.copy()
        training_types = TrainingType.objects.filter(zone = data['planned_type_of_training'])
        local_data['planned_type_of_training'] = training_types[0].full_type_as_string

        data_elements = local_data.values()

        # for table_row in table_rows :
        self.assertGreater(len(table_rows), row_to_check, 'table only has ' + str(len(table_rows)) + ' rows and you wanted to check row ' + str(row_to_check))
        for element in data_elements :
            self.assertTrue(element in table_rows[row_to_check].text, element + ' not in ' + table_rows[row_to_check].text)

    def test_enter_training_data(self) :
        # user gets the url
        self.browser.get(self.live_server_url)
        # user enters a first set of data and checks if the data is receptioned by the system
        self.user_sees_inputfields_and_enters_data(self.first_training_session)
        # user sees the row in the table on the page matching the data entered
        self.check_entered_row_of_data_on_screen(1, self.first_training_session)
        
        # user enters a second set of data checks if the data is receptioned by the system
        self.user_sees_inputfields_and_enters_data(self.second_training_session)
        # user sees both rows in the table on the page matching the data from the second training session
        self.check_entered_row_of_data_on_screen(1, self.first_training_session)
        self.check_entered_row_of_data_on_screen(2, self.second_training_session)
        
        # user closes the browser and reopens, to see his previously entered data
        self.browser.quit()
        self.browser = Chrome()
        self.browser.implicitly_wait(3)
        # user gets the url
        self.browser.get(self.live_server_url)
        self.check_entered_row_of_data_on_screen(1, self.first_training_session)
        self.check_entered_row_of_data_on_screen(2, self.second_training_session)

    def test_web_page_is_loaded(self) :
        # user gets the url
        self.browser.get(self.live_server_url)
        # user sees the title in the browser window
        self.assertIn('Runners Log', self.browser.title)

    def test_css_is_used(self) :
        # user sees the table layout of the input elements

        # The "add training" part of the website is put in a table layout, 3 x 3. The "Distance" label needs to have
        # a different x location than the "Date" label. The "Date" label is in column 1, the "Distance" label is in
        # column 2. If the css should not be used, these labels would have the same x location, thus failing the
        # test.
        self.browser.get(self.live_server_url)

        labels = self.browser.find_elements_by_class_name('label')
        
        for label in labels :
            if label.text == 'Distance' :
                distance_x = label.location['x']
            if label.text == 'Date' :
                date_x = label.location['x']

        self.assertNotEqual(date_x, distance_x, 'label \'Date\' and label \'Distance\' have the same x-coordinate - CSS possibly not loaded')
