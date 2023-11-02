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

class Logout(unittest.TestCase):

    result_flag = False

    def setUp(self):

        self.driver = webdriver.Remote(iosConfig.getURL(), iosConfig.getCapabilities())

        pass
    
    def updateTestrailTestRun(self, project_name, testRun_name, case_id, case_name, result_flag):  

        test_run_id = testrail_integration.get_run_id(testRun_name,project_name)

        if (result_flag):
            msg = "PASSED: " + case_name
        else:
            msg = "FAILED: " + case_name

        testrail_integration.update_testrail(case_id,test_run_id, result_flag, msg=msg)

        pass


    def test_logout(self):
        
        case_id = 18

        maxWait = 60
        
        # create directory to store screenshots
        if not (os.path.exists('./screenshots')):
            os.makedirs('./screenshots')
        
        self.driver.save_screenshot('./screenshots/logout_landing.png')
            
        # Click PROFILE button
        
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('label == "Profile"')):
                    self.driver.find_element_by_ios_predicate('label == "Profile"').click()
                    break
                    
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (profile) button")
                    self.driver.save_screenshot('./screenshots/logout_error_landing.png')
                    
                    break
                time.sleep(1)
        
        #Scroll down and click LOGOUT link
        self.driver.execute_script("mobile: scroll", {"direction":'down'})
        
        # click LOG OUT link
        for x in range (0, maxWait):
        
            try:
                if (self.driver.find_element_by_ios_predicate('label == "Log Out"')):
                    self.driver.find_element_by_ios_predicate('label == "Log Out"').click()
                    break
                    
            except:
                if (x + 1 == maxWait):
                    print ("ERROR: Could not locate (logout) link")
                    self.driver.save_screenshot('./screenshots/logout_error_logoutLink.png')
                    break
                time.sleep(1)
        
        #Click LOGOUT button to confirm
        wSize = self.driver.get_window_size("current")
        wWidth = wSize["width"]
        wHeight = wSize["height"]
        time.sleep(5)
        #self.driver.find_element_by_name('cancelButton').click()
        self.driver.tap([(wWidth * 0.25, wHeight * 0.60)])
        
        #wait for main page to load and verify test is successful
        for x in range (0, maxWait):
            
            try:
                if (self.driver.find_element_by_ios_predicate('label == "Sign up"')):
                    Logout.result_flag = True
                    self.driver.save_screenshot('./screenshots/logout_passed.png')
                    break
            except:
                if (x + 1 == maxWait):
                    Logout.result_flag = False
                    self.driver.save_screenshot('./screenshots/logout_failed.png')
                    break
                time.sleep(1)
        
        self.updateTestrailTestRun(iosConfig.getProjectName(),iosConfig.getTestRun(), case_id, 'Logout', Logout.result_flag)

        pass

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Logout)
    unittest.TextTestRunner(verbosity=2).run(suite)
