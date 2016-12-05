from selenium.webdriver import Firefox
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys

class NewTrainingData(LiveServerTestCase) :
    def setUp(self) :
        # TODO setup lists with test data here, and make the 2 methods user_sees and check_entered accept these lists
        self.browser = Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) :
        self.browser.quit()

    def user_sees_inputfields_and_enters_data(self, distance, executed_time, in_zone, average_heart_rate) :
        # user sees 4 edit boxes to enter distance, executed time, in zone and average HR 
        distance_editbox = self.browser.find_element_by_name('distance')
        self.assertIsNotNone(distance_editbox)
        
        executed_time_editbox = self.browser.find_element_by_name('executed_time')
        self.assertIsNotNone(executed_time_editbox)

        in_zone_editbox = self.browser.find_element_by_name('in_zone')
        self.assertIsNotNone(in_zone_editbox)

        average_heart_rate_editbox = self.browser.find_element_by_name('average_heart_rate')
        self.assertIsNotNone(average_heart_rate_editbox)

        # TODO: user sees km, bpm, .... next to the edit boxes

        # user sees a submit button with the text 'submit' on it
        submit_button = self.browser.find_element_by_id('submit_button')
        self.assertEqual(submit_button.get_attribute('value'), 'submit')

        # user enters data in the 4 fields an presses submit
        # TODO : user sees he gets redirected to the same home url
        distance_editbox.send_keys(distance)
        executed_time_editbox.send_keys(executed_time)
        in_zone_editbox.send_keys(in_zone)
        average_heart_rate_editbox.send_keys(average_heart_rate)
        submit_button.submit()
        
       
    def check_entered_data_on_screen(self, data) :
        # user sees a table and an entry in a table on the page with the entered data 
        try :
            table_rows = self.browser.find_elements_by_tag_name('tr')
        except StaleElementReferenceException :
            # wait for all the elements to be attached to the DOM (stale exception selenium)
            self.browser.implicitly_wait(3)
            table_rows = self.browser.find_elements_by_tag_name('tr')

        # user checks if the number of rows entered equals the number of rows displayed in the table
        self.assertEqual(len(table_rows), len(data), 'not all data records are in the DB')
        for table_row in table_rows :
            self.assertIn(table_row.text, data, 'runners record wrong data or not in DB')

    def test_enter_training_data(self) :
        # user gets the url
        self.browser.get(self.live_server_url)
        # user enters a first set of data and checks if the data is receptioned by the system
        self.user_sees_inputfields_and_enters_data('9', '00:46:48', '00:38:42', '162')
        # user sees the row in the table on the page matching the data entered
        self.check_entered_data_on_screen(['9.0 0:46:48 0:38:42 162'])
        
        # user enters a second set of data checks if the data is receptioned by the system
        self.user_sees_inputfields_and_enters_data('14.182', '01:08:53', '00:52:23', '159')
        # user sees both rows in the table on the page matching the data from the second training session
        self.check_entered_data_on_screen(['9.0 0:46:48 0:38:42 162', '14.182 1:08:53 0:52:23 159'])
        
        # user closes the browser and reopens, to see his previously entered data
        self.tearDown()
        self.setUp()
        # user gets the url
        self.browser.get(self.live_server_url)
        self.check_entered_data_on_screen(['9.0 0:46:48 0:38:42 162', '14.182 1:08:53 0:52:23 159'])

    def test_web_page_is_loaded(self) :
        # user gets the url
        self.browser.get(self.live_server_url)
        # user sees the title in the browser window
        self.assertIn('Runners Log', self.browser.title)
