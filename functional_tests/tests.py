from selenium.webdriver import Chrome
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys

class NewTrainingData(LiveServerTestCase) :
    def setUp(self) :
        # TODO setup lists with test data here, and make the 2 methods user_sees and check_entered accept these lists
        self.browser = Chrome()
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
        self.assertEqual(submit_button.get_attribute('value'), 'Save')

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

        # the header row is static, it is of no use to us, so we delete it
        del table_rows[0]
        self.assertEqual(len(table_rows), len(data), 'not all data records are in the DB')
        counter = 0
        for table_row in table_rows :
            elements = data[counter].split(' ')
            counter += 1
            for element in elements :
                self.assertTrue(element in table_row.text, element + ' not in ' + table_row.text)

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

    def test_css_is_used(self) :
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
