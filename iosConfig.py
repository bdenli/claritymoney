'''
Created on Jun 19, 2017

@author: basak
'''

from appium import webdriver
import os
import shutil
import testrail_integration
import iosConfig
import time
import datetime

runName = "null"
projectName = "null"

report = "null"
path = "null"

def cleanup(project_name):

    # create directory to store screenshots
    if (os.path.exists('./screenshots')):
        shutil.rmtree('./screenshots')
        os.makedirs('./screenshots')
    else:
        os.makedirs('./screenshots')
    
    # create directory to store reports
    if (os.path.exists('./reports')):
        shutil.rmtree('./reports')
        os.makedirs('./reports')
    else:
        os.makedirs('./reports')

    global runName
    date = datetime.datetime.now()
    runNum = '%s%s%s%s-%s ' % (date.month, date.day, date.year, date.hour, date.minute)
    runName = testrail_integration.create_new_run(project_name, runNum)

    global projectName
    projectName = project_name

    return runName

    pass


def createNewReport(project_name):

        global report
        global path

        path = "./reports/"
        
        runName = cleanup(project_name)
        report = 'report_' + runName + '.txt'

        with open(os.path.join(path, report), 'w') as temp_file:
            temp_file.write("REPORT" + "\n" + "\n")

        #file = open(report, 'w')

        return None

        pass


def create_webdriver():

    wd = webdriver.Remote(getURL(), getCapabilities())
    
    return wd

    pass

def getAppPath():
    
    #app_path = "../../../../Desktop/Clarity Money.app" # for local testing
    app_path = "../tests/build/Clarity Money.app" # for remote testing
    
    return app_path
            
    pass

def getURL():

    URL = "http://0.0.0.0:4723/wd/hub"

    return URL

    pass

def getCapabilities():

    desired_caps = {
            "platformName": "iOS",
            "platformVersion": "10.2",
            "deviceName": "iPhone 7",
            "automationName": "XCUITest",
            "app": os.path.abspath(getAppPath()),
            "noReset": "true"
        }
    return desired_caps

    pass

def getTestRun():

    global runName
    _runName = runName

    return _runName
            
    pass

def getProjectName():

    global projectName
    _projectName = projectName

    return _projectName

    pass