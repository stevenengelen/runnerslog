from selenium.webdriver import Firefox
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys

class NewTrainingData(LiveServerTestCase) :
    def setUp(self) :
        self.browser = Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self) :
        self.browser.quit()

    def test_web_page_is_loaded(self) :
        # load the main page of the application in a web browser
        self.browser.get(self.live_server_url)
        self.assertIn('Runners Log', self.browser.title)

    def test_enter_training_data(self) :
        self.browser.get(self.live_server_url)
        
        # user sees 4 edit boxes to enter distance, executed time, in zone and average HR
        distance_editbox = self.browser.find_element_by_id('id_new_distance')
        self.assertEqual(distance_editbox.get_attribute('placeholder'), 'Distance')

        executed_time_editbox = self.browser.find_element_by_id('id_new_executed_time')
        self.assertEqual(executed_time_editbox.get_attribute('placeholder'), 'Executed Time')

        in_zone_editbox = self.browser.find_element_by_id('id_new_in_zone')
        self.assertEqual(in_zone_editbox.get_attribute('placeholder'), 'In Zone')

        average_heart_rate_editbox = self.browser.find_element_by_id('id_new_average_heart_rate')
        self.assertEqual(average_heart_rate_editbox.get_attribute('placeholder'), 'Average Heart Rate')

        # TODO: user sees km, bpm, .... next to the edit boxes

        # user sees a submit button
        submit_button = self.browser.find_element_by_id('submit')
        self.assertEqual(submit_button.get_attribute('value'), 'submit')
        # user enters data in the 4 fields an presses submit
        # TODO : user sees he gets redirected to the same home url
        # user sees an entry in a table on the page with the entered data
        distance_editbox.send_keys('9')
        executed_time_editbox.send_keys('00:46:48')
        in_zone_editbox.send_keys('00:38:42')
        average_heart_rate_editbox.send_keys('162')
        submit_button.submit()
        
        table = self.browser.find_element_by_id('id_training_table')
        
        self.assertIn('9.0', table.text)
        self.assertIn('0:46:48', table.text)
        self.assertIn('0:38:42', table.text)
        self.assertIn('162', table.text)

        self.browser.get(self.live_server_url)
        
        # user sees 4 edit boxes to enter distance, executed time, in zone and average HR
        distance_editbox = self.browser.find_element_by_id('id_new_distance')
        self.assertEqual(distance_editbox.get_attribute('placeholder'), 'Distance')

        executed_time_editbox = self.browser.find_element_by_id('id_new_executed_time')
        self.assertEqual(executed_time_editbox.get_attribute('placeholder'), 'Executed Time')

        in_zone_editbox = self.browser.find_element_by_id('id_new_in_zone')
        self.assertEqual(in_zone_editbox.get_attribute('placeholder'), 'In Zone')

        average_heart_rate_editbox = self.browser.find_element_by_id('id_new_average_heart_rate')
        self.assertEqual(average_heart_rate_editbox.get_attribute('placeholder'), 'Average Heart Rate')

        # TODO: user sees km, bpm, .... next to the edit boxes

        # user sees a submit button
        submit_button = self.browser.find_element_by_id('submit')
        self.assertEqual(submit_button.get_attribute('value'), 'submit')

        # user enters a second training session
        distance_editbox.send_keys('14.182')
        executed_time_editbox.send_keys('01:08:53')
        in_zone_editbox.send_keys('00:52:23')
        average_heart_rate_editbox.send_keys('159')
        submit_button.submit()

        # user sees a second row in the table on the page matching the data from the second training session
        table = self.browser.find_element_by_id('id_training_table')
        self.assertIn('14.182', table.text)
        self.assertIn('1:08:53', table.text)
        self.assertIn('0:52:23', table.text)
        self.assertIn('159', table.text)
        
        # user also sees the previously entered row
        self.assertIn('9.0', table.text)
        self.assertIn('0:46:48', table.text)
        self.assertIn('0:38:42', table.text)
        self.assertIn('162', table.text)

    def test_display_data_over_sessions(self) :
        # user closes the browser and reopens, to see his previously entered data
        self.browser.quit()
        self.browser = Firefox()
        self.browser.get(self.live_server_url)
        
        table = self.browser.find_element_by_id('id_training_table')
        self.assertIn('14.182', table.text)
        self.assertIn('1:08:53', table.text)
        self.assertIn('0:52:23', table.text)
        self.assertIn('159', table.text)
        
        self.assertIn('9.0', table.text)
        self.assertIn('0:46:48', table.text)
        self.assertIn('0:38:42', table.text)
        self.assertIn('162', table.text)
