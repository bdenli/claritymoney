lib'''
Created on Jun 19, 2017

@author: basak
'''
import unittest
from appium import webdriver
import os
import time
import testrail_integration
import iosConfig

class Signup(unittest.TestCase):

    result_flag = False

    def setUp(self):

        self.driver = webdriver.Remote(iosConfig.getURL(), iosConfig.getCapabilities())

        pass
    
    def _send_keys (self, keys):
        
        for k in keys:
            if (k.isdigit()):
                self.driver.find_element_by_name("more").click()
                self.driver.find_element_by_name(k).click()
                self.driver.find_element_by_name("more").click()
            else:
                self.driver.find_element_by_name(k).click()
            
        pass

    def updateTestrailTestRun(self, project_name, testRun_name, case_id, case_name, result_flag):  

        test_run_id = testrail_integration.get_run_id(testRun_name,project_name)

        if (result_flag):
            msg = "PASSED: " + case_name
        else:
            msg = "FAILED: " + case_name

        testrail_integration.update_testrail(case_id, test_run_id, result_flag, msg=msg)

        pass

    def test_signup(self):

        case_id = 1

        email = "cmbasak01@gmail.com"
        password = "guldur"
        fName = "Clarity"
        lName = "Money"
        maxWait = 60
        
        # create directory to store screenshots
        if not (os.path.exists('./screenshots')):
            os.makedirs('./screenshots')
        
        self.driver.save_screenshot('./screenshots/signup_landing.png')
        
        # click SIGN UP button
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('label == "Sign up"')):
                    self.driver.find_element_by_ios_predicate('label == "Sign up"').click()
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (sign up) button")
                    self.driver.save_screenshot('./screenshots/signup_error_landing.png')
                    break
                time.sleep(1)
        
        # enter email
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('value == "Email"')):
                    self.driver.find_element_by_ios_predicate('value == "Email"').click()
                    self._send_keys(email)
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (email) text field")
                    self.driver.save_screenshot('./screenshots/signup_error_email.png')
                    break
                time.sleep(1)
        
        # enter password
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('value == "Password"')):
                    self.driver.find_element_by_ios_predicate('value == "Password"').click()
                    self._send_keys(password)
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (password) text field")
                    self.driver.save_screenshot('./screenshots/signup_error_password.png')
                    break
                time.sleep(1)
                
        # enter first name
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('value == "First name"')):
                    self.driver.find_element_by_ios_predicate('value == "First name"').click()
                    self._send_keys(fName)
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (first name) text field")
                    self.driver.save_screenshot('./screenshots/signup_error_fName.png')
                    break
                time.sleep(1)
        
        # enter last name
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('value == "Last name"')):
                    self.driver.find_element_by_ios_predicate('value == "Last name"').click()
                    self._send_keys(lName)
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (last name) text field")
                    self.driver.save_screenshot('./screenshots/signup_error_lName.png')
                    break
                time.sleep(1)
                
        # click DONE button
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_name("Done")):
                    self.driver.find_element_by_name("Done").click()
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (done) button")
                    self.driver.save_screenshot('./screenshots/signup_error_doneButton.png')
                    break
                time.sleep(1)
        
        # verify test result
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('label == "Profile"')):
                    Signup.result_flag = True
                    self.driver.save_screenshot('./screenshots/signup_passed.png')
                    break
            except:
                if (x + 1 == maxWait):
                    Signup.result_flag = False
                    self.driver.save_screenshot('./screenshots/signup_failed.png')
                    break
                time.sleep(1)

        self.updateTestrailTestRun(iosConfig.getProjectName(),iosConfig.getTestRun(), case_id, 'Signup', Signup.result_flag)
            
        pass

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Signup)
    unittest.TextTestRunner(verbosity=2).run(suite)
