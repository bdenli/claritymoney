'''
Created on Jun 19, 2017

@author: basak
'''
import unittest
from appium import webdriver
import os
import time
import testrail_integration
import iosConfig

class Signin(unittest.TestCase):

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

        testrail_integration.update_testrail(case_id,test_run_id, result_flag, msg=msg)

        pass

    def test_signin(self):
        
        case_id = 17

        email = "claritymoneyqa@gmail.com"
        password = "tester12"
        maxWait = 60
        
        # create directory to store screenshots
        if not (os.path.exists('./screenshots')):
            os.makedirs('./screenshots')
        
        self.driver.save_screenshot('./screenshots/signin_landing.png')
        
        #click ALREADY HAVE AN ACCOUNT? button
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('label CONTAINS "Already have an account"')):
                    self.driver.find_element_by_ios_predicate('label CONTAINS "Already have an account"').click()
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate ALREADY HAVE AN ACCOUNT? link")
                    self.driver.save_screenshot('./screenshots/signin_error_landing.png')
                    break
                time.sleep(1)
        
        # enter EMAIL
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('value == "Email"')):
                    self.driver.find_element_by_ios_predicate('value == "Email"').click()
                    self._send_keys(email)
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate email text field")
                    self.driver.save_screenshot('./screenshots/signin_error_email.png')
                    break
                time.sleep(1)
                
        # enter PASSWORD
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('value == "Password"')):
                    self.driver.find_element_by_ios_predicate('value == "Password"').click()
                    self._send_keys(password)
                    break
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate password text field")
                    self.driver.save_screenshot('./screenshots/signin_error_password.png')
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
                    print ("ERROR: Could not locate DONE button")
                    self.driver.save_screenshot('./screenshots/signin_error_done.png')
                    break
                time.sleep(1)
        
        #wait for main page to load and verify that test is successful
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('label == "Profile"')):
                    Signin.result_flag = True
                    self.driver.save_screenshot('./screenshots/signin_passed.png')
                    break
            except:
                if (x + 1 == maxWait):
                    Signin.result_flag = False
                    self.driver.save_screenshot('./screenshots/signin_failed.png')
                    break
                time.sleep(1)
        
        self.updateTestrailTestRun(iosConfig.getProjectName(),iosConfig.getTestRun(), case_id, 'Signin', Signin.result_flag)

        pass

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Signin)
    unittest.TextTestRunner(verbosity=2).run(suite)
