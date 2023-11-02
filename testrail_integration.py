"""
TestRail integration
"""

import os
import testrail
import iosConfig
import testrail_integration

count = 0

def get_testrail_client():

    #Get the TestRail Url
        client = testrail.APIClient('https://claritymoney.testrail.net/')
    
	    #Get and set the TestRail User and Password
        client.user = 'basak@claritymoney.com'
        client.password = 'tester12'
 
        return client

def update_testrail(case_id,run_id,result_flag,msg=""):

    #"Update TestRail for a given run_id and case_id"
        update_flag = False
    
	    #Get the TestRail client account details
        client = get_testrail_client()
 
        #Update the result in TestRail using send_post function. 
        #Parameters for add_result_for_case is the combination of runid and case id. 
        #status_id is 1 for Passed, 2 For Blocked, 4 for Retest and 5 for Failed
        status_id = 1 if result_flag is True else 5
 
        if run_id is not None:
            try:
                result = client.send_post(
                    'add_result_for_case/%s/%s'%(run_id,case_id),
                    {'status_id': status_id, 'comment': msg })
            except Exception,e:
                print 'Exception in update_testrail() updating TestRail.'
                print 'PYTHON SAYS: '
                print e
            else:
                print 'Updated test result for case: %s in test run: %s with msg: %s'%(case_id,run_id,msg)
 
        return update_flag

def nextRunNum():
    
    global count
    count += 1

    return count

def create_new_run(project_name, runNum):

    client = get_testrail_client()

    runName = "Build " + runNum

    client.send_post('add_run/%s'%(get_project_id(project_name)), {
	"name": runName,
	"include_all": False,
	"case_ids": [3,28,30,37,38,39,40,41,42,4,43,44,45,20,46,47,
    48,50,51,52,53,54,21,22,55,56,23,57,58,59,60,61,62,
    63,24,64,65,66,67,68,69,70,25,71,72,26,73,74,75,76,77,
    78,79,27,80,81,82,83,84,29,87,88,89,90,91,92,93,94,95,
    96,31,97,32,98,99,100,101,102,33,103,104,105,106,34,85,
    86,35,107,108,36,109,110,111,112,113,114,115,116,117,118,
    119,120,121,122,123,124,142,143,144,145,146,147,148,149,
    150,151,152,153,154,155,156,157,158,159,160,161,162,163,
    164,165,166,167,168,169,170,171,172,173,174,175,176,177,
    178,179,180,181,182,183,184,185,186,187,188,189,190,191,
    192,193,194,195,196,197,198,199,200,201,202,203,204,205,
    206,207,208,209,210,211,212,213,214,215,216,217,218,219,
    220,221,222,223,224,225,226,227,228,229]})
    
    return runName

def get_project_id(project_name):
    
    #"Get the project ID using project name"
        client = get_testrail_client()
        project_id=None
        projects = client.send_get('get_projects')
        for project in projects:
            if project['name'] == project_name: 
                project_id = project['id']
                #project_found_flag=True
                break
        return project_id
 
def get_run_id(test_run_name,project_name):

    #"Get the run ID using test name and project name"
        run_id=None
        client = get_testrail_client()
        project_id = get_project_id(project_name)

        try:
            test_runs = client.send_get('get_runs/%s'%(project_id))
        except Exception,e:
            print 'Exception in update_testrail() updating TestRail.'
            print 'PYTHON SAYS: '
            print e
            return None
        else:
            for test_run in test_runs:
                #if str(test_run['name']) == str(test_run_name):
                run_id = test_run['id']
                break
            return run_id