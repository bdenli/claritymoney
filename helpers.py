'''
Created on Jun 19, 2017
@author: basak
'''
import unittest
from appium import webdriver
import os
import time
from random import randint
import testrail_integration
import iosConfig
from enum import Enum


maxWait = 10 # max wait time
sDuration = 0 # swipe duration
photoNum = 0 # unique id for screenshots

Elements = {

        # buttons

        'cta_subscription' : 'subscriptionTakeALookButton',
        'cta_whatDidISpend' : 'whatDidISpendTile takeALookButton',
        'cta_transfers' : 'transfersTile DoItButton',
        'cta_notifications' : 'notificationsTile turnOnNotificationsButton',
        'cta_lowerBills' : 'lowerBillsTile checkItOutButton',
        'cta_savings' : 'savingsAccountTile doItButton',
        'cta_referFriend' : 'referFriendTile referFriendButton',
        'try_demo' : 'welcomePage tryDemoButton',
        'exit_demo' : 'demoMode exitButton',
        '_previous' : 'previousCategoryButton',
        '_next' : 'nextCategoryButton',
        'dismiss' : 'CloseIconFilled',
        'cancel' : 'Cancel',
        'done' : 'Done',
        'okay' : 'Okay',
        'picker_done' : 'pickerDoneButton',
        'transfer' : 'transfersTile transferButton',
        'got_it' : 'transfersTile gotItButton',
        'see_all_transfers' : 'transfersTile seeAllTransfersButton',
        'vendor' : 'whatDidISpendTile vendorButton',
        'time_range' : 'whatDidISpendTile filterButton',
        'amount' : 'transferTile amountButton',

        # back buttons

        'back_balance' : 'ClarityMoney.AccountsView',
        'back_dailySummary' : 'ClarityMoney.DailySummaryDetailView',
        'back_transactions' : '_TtGC12ClarityMoney32TransactionsDetailView',
        'back_incomeThisMonth' : 'ClarityMoney.IncomeThisMonthDetailView',
        'back_monthlyIncome' : 'ClarityMoney.LTSAndPieChartDetailView',
        'back_categorySpending' : 'ClarityMoney.CategorySpendingDetailView',
        'back_cancelSubscription' : 'ClarityMoney.MonthlySubscriptionsView',
        'back_cancelSubscriptionForm' : 'Cancel Subscription',
        'back_whatDidISpend' : 'ClarityMoney.TrackMyExpenseDetailView',
        'back_transfers' : 'ClarityMoney.TransfersView',
        'back_creditScore' : 'ClarityMoney.CreditScoreDetailView',
        'back_lowerBills' : 'ClarityMoney.BillsharkDetailView',
        'back_lowerBillsForm' : 'Account Information',
        'back_creditCards' : 'ClarityMoney.CreditCardDetailView',
        'back_savings' : 'ClarityMoney.SavingsAccountView',
        'back_referFriend' : 'ClarityMoney.ReferFriendDetailView',
        'back_thankYou' : 'ClarityMoney.ThankYouTileDetailView',
        'back_register': 'ClarityMoney.RegisterView',

        'cell': 'transaction row',

        # filters

        'filter_category': 'categorySpendingFilter',
        'filter_sort' :'sortButton',
        'filter_main' : 'filterButton',
        'filter_transaction': 'Transactions Filter',

        # others

        'pencil': 'Category',
        'switch': 'Switch',
        'search_field': 'Search All'
}         


def cancel_subscription(driver, _selector):

        # need coordination for CTA button
        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])

        result_flag = True
        msg = "Msg: Successfully canceled a subscription"

        result_flag_arr = []
        msg_arr = []

        #tap cancel

        result_flag_item, msg_item = tap_element(driver, 'Cancel')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'cancel button')

        #tap field
        result_flag_item, msg_item = tap_list_item(driver, 6)
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'list item')

        # enter last 4 digits and tap <done> button on the keyboard

        result_flag_item, msg_item = tap_element(driver, '1')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, '2')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, '3')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, '4')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, 'Done')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'Done')

        driver.tap([(wWidth/2, wHeight * 0.75)]) # tap <submit> button

        #tap okay
        result_flag_item, msg_item = tap_element(driver, 'Okay')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'Okay button')

        for i in range (0,len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, 'Cancel Subscription', 71, "Cancel Subscription Tile: cancel a subscription", result_flag, msg)
        

        pass


def dismiss_tile_lightX(driver, _selector):

        find_element(driver, 'CloseIconFilled')
        tap_element(driver, 'CloseIconFilled')

        pass


def dismiss_tile_darkX(driver, _selector):
        
        find_element(driver, 'xButton_darkGrey')
        tap_element(driver, 'xButton_darkGrey')
            
        pass


def do_better(driver, _selector):

        # to-do


        pass


def do_nothing(driver, _selector):

        pass


def edit_category(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully edited category"

        result_flag_arr = []
        msg_arr = []

        try:
                result_flag_item, msg_item = tap_element(driver, Elements['cell'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        time.sleep(1)
                        take_screenshot(driver, 'cell')
                
                try:
                        result_flag_item, msg_item = tap_element(driver, Elements['pencil'])
                        result_flag_arr.append(result_flag_item)
                        msg_arr.append(msg_item)
                        if (result_flag_item == False):
                                time.sleep(1)
                                take_screenshot(driver, 'pencil icon')

                        # to do: change picker selection

                        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
                        result_flag_arr.append(result_flag_item)
                        msg_arr.append(msg_item)
                        if (result_flag_item == False):
                                time.sleep(1)
                                take_screenshot(driver, 'picker_done')

                        result_flag_item, msg_item = tap_element(driver, Elements['cell'])
                        result_flag_arr.append(result_flag_item)
                        msg_arr.append(msg_item)
                        if (result_flag_item == False):
                                time.sleep(1)
                                take_screenshot(driver, 'cell')
                        
                except:
                        scroll_down(driver)
        except:
                scroll_to_element(driver,Elements['cell'])

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, 'edit category', TestrailMap_editCategory[_selector], TileDict_reverse[_selector] + ": edit category", result_flag, msg)

        pass


def edit_category_2(driver, _selector):

        tap_list_item(driver, 1) # go to 2nd detail view

        try:

                tap_element(driver, Elements['cell'])
                try:
                        tap_element(driver, Elements['pencil'])
                        # to do: change picker selection
                        tap_element(driver, Elements['picker_done'])
                        tap_element(driver, Elements['cell'])
                        tap_back_2(driver) # go back to 1st level detail
                except:
                        scroll_down(driver)
        except:
                scroll_to_element(driver,Elements['cell'])


        pass




def edit_category_filter(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully editted category filter in detail view"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver, Elements['filter_category'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'category filter')

        # to do : change picker selection

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'picker_done')


        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 64, TileDict_reverse[_selector] + ": edit category filter in detail view", result_flag, msg)

        pass

def edit_transaction_filter(driver, _selector):


        result_flag = True
        msg = "Successfully editted transaction filter in detail view"

        result_flag_arr = []
        msg_arr = []

        try:

                result_flag_item, msg_item = tap_element(driver, Elements['filter_transaction'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        time.sleep(1)
                        take_screenshot(driver, 'transaction filter')

                # to do : change picker selection

                result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        time.sleep(1)
                        take_screenshot(driver, 'picker done')
        
        except:
                result_flag_arr.append(False)
                msg_arr.append("Could not edit transaction filter in detail view")
                if (result_flag_item == False):
                        time.sleep(1)
                        take_screenshot(driver, _selector)

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, TestrailMap_editTransFilter[_selector], TileDict_reverse[_selector] + ": edit transaction filter in detail view", result_flag, msg)


        pass


def edit_transaction_filter_2(driver, _selector):

        tap_list_item(driver, 1) # go to 2nd detail view
        tap_element(driver, Elements['filter_transaction'])
        
        # to do : change picker selection
        
        tap_element(driver, Elements['picker_done'])
        tap_back_2(driver) # go back to 1st level detail

        pass



def edit_order(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully editted order in detail view"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver, Elements['filter_sort'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'sort filter')

        # to do : change picker selection

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'picker_done')

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, TestrailMap_editOrder[_selector], TileDict_reverse[_selector] + ": edit order in detail view", result_flag, msg)

        pass


def edit_order_2(driver, _selector):

        tap_list_item(driver, 1) # go to 2nd detail view
        tap_element(driver, Elements['filter_sort'])
        # to do : change picker selection
        tap_element(driver, Elements['picker_done'])
        tap_back_2(driver) # go back to 1st level detail

        pass


def edit_vendor_pill(driver, _selector):


        result_flag = True
        msg = "Msg: Successfully editted vendor pill in detail view"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver,'whatDidISpendTile vendorButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'whatDidISpendTile vendorButton')

        # to-do: change selection

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'picker_done')

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 75, TileDict_reverse[_selector] + ": edit vendor pill in detail view", result_flag, msg)

        pass


def edit_filter_pill(driver, _selector):

        result_flag = True
        msg = "Successfully editted filter pill in detail view"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver, 'whatDidISpendTile filterButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'whatDidISpendTile filterButton')

        # to-do: change selection

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'picker_done')

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 76 , TileDict_reverse[_selector] + ": edit filter pill in detail view", result_flag, msg)

        pass


def transfer_money(driver, _selector):

        # need coordination for checkbox
        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])

        result_flag = True
        msg = "Successfully transferred money"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver, 'transferTile amountButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'transferTile amountButton')

        result_flag_item, msg_item = tap_element(driver, '1')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, '2')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                time.sleep(1)
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, '3')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, '4')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'key')

        result_flag_item, msg_item = tap_element(driver, 'Done')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'Done')

        driver.tap([(wWidth * 0.1, wHeight * 0.80)]) # tap checkbox

        result_flag_item, msg_item = tap_element(driver, 'transfersTile transferButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'transfersTile transferButton')

        result_flag_item, msg_item = tap_element(driver, 'transfersTile gotItButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'transfersTile gotItButton')

        result_flag_item, msg_item = tap_element(driver, 'transfersTile seeAllTransfersButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'transfersTile seeAllTransfersButton')

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)

        verify_test(driver, 'Transfer money', 80, "Transfer Tile: transfer money", result_flag, msg)

        pass



def enter_demo(driver):

        result_flag, msg = tap_element(driver, Elements['try_demo'])
        
        pass


def exit_demo(driver):

        tap_element(driver,Elements['exit_demo'])
        tap_back_2(driver)

        pass



def find_element(driver, _selector):

        global maxWait
        _found = False
        _element = None

        for x in range (0, maxWait):
                
                try:
                        
                        if (driver.find_element_by_name(_selector)):
                                _element = driver.find_element_by_name(_selector)
                                _found = True
                                break
                except:
                        if (x + 1 == maxWait):
                                _found = False
                                break

                        time.sleep(1)
        return _found, _element
        pass


def find_element_by_class(driver, _selector):

        global maxWait
        _found = False
        _element = None

        for x in range (0, maxWait):
                
                try:
                        
                        if (driver.find_element_by_class_name(_selector)):
                                _element = driver.find_element_by_class_name(_selector)
                                _found = True
                                break
                except:
                        if (x + 1 == maxWait): 
                                _found = False
                                break

                        time.sleep(1)
        return _found, _element
        pass


def find_element_by_predicate(driver, _selector):

        global maxWait
        _found = False
        _element = None

        label = 'label CONTAINS' + " \"" + _selector + "\" "
        value = 'value ==' + " \"" + _selector + "\" "

        for x in range (0, maxWait):
                
                try:
                        
                        if (driver.find_element_by_ios_predicate(label)):
                                _element = driver.find_element_by_ios_predicate(label)
                                _found = True
                                break
                        elif(driver.find_element_by_ios_predicate(value)):
                                _element = driver.find_element_by_ios_predicate(value)
                                _found = True
                                break
                                
                except:
                        if (x + 1 == maxWait):  
                                _found = False  

                        time.sleep(1)
        return _found, _element
        pass



def loop_category(driver, _selector):


        result_flag = True
        msg = "Msg: Successfully looped through categories"

        result_flag_arr = []
        msg_arr = []

        try:

                result_flag_item, msg_item = tap_element(driver, Elements['_previous'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, '_previous')

                result_flag_item, msg_item = tap_element(driver, Elements['_previous'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, '_previous')

                result_flag_item, msg_item = tap_element(driver, Elements['_previous'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, '_previous')

                result_flag_item, msg_item = tap_element(driver, Elements['_next'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, '_next')

                result_flag_item, msg_item = tap_element(driver, Elements['_next'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, '_next')

                result_flag_item, msg_item = tap_element(driver, Elements['_next'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, '_next')

        except:
                result_flag_arr.append(False)
                msg_arr.append("Could not loop through categories")
                if (result_flag_item == False):
                        take_screenshot(driver, 'loop categories')

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 67, TileDict_reverse[_selector] + ": loop category in detail view", result_flag, msg)

        pass


def lower_bill(driver, _selector):

        # need coordinates for <negotiate now> button
        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])

        result_flag = True
        msg = "Msg: Successfully lowered a bill"

        result_flag_arr = []
        msg_arr = []

        try:

                result_flag_item, msg_item = tap_element(driver, 'lowerBillsTile doItButton')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'lowerBillsTile doItButton')

                result_flag_item, msg_item = tap_list_item(driver, 10)
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'list item')

                _send_keys(driver, "One")

                result_flag_item, msg_item = tap_element(driver, "Done")
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'Done')

                result_flag_item, msg_item = tap_list_item(driver, 11)
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'list item')

                _send_keys(driver, "Two")

                result_flag_item, msg_item = tap_element(driver, "Done")
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'Done')

                driver.tap([(wWidth/2, wHeight * 0.95)]) # tap <negotiate now> button using coordinates

                result_flag_item, msg_item = tap_element(driver, 'okayButton') # confirmation
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'okayButton')

        except:
                result_flag_arr.append(False)
                msg_arr.append("Could not lower a bill")
                if (result_flag_item == False):
                        take_screenshot(driver, _selector)

        
        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 87 , TileDict_reverse[_selector] + ": lower a bill", result_flag, msg)


        pass


def open_close_savings(driver, _selector):

        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])

        result_flag = True
        msg = "Msg: Successfully opened/closed savings account"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_amount_pill(driver, 'null')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'amount pill')

        result_flag_item, msg_item = tap_frequency_pill(driver, 'null')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'frequency pill')

        result_flag_item, msg_item = tap_goal_pill(driver, 'null')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'goal pill')

        result_flag_item, msg_item = tap_account_pill(driver, 'null')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'account pill')

        # open account
        time.sleep(3)
        if (driver.find_elements_by_class_name('Other')[4]):
                driver.find_elements_by_class_name('Other')[4].click() # tap <submit> button
                result_flag_arr.append(True)
                msg_arr.append("Successfully tapped <submit> button")

        else:
                result_flag_arr.append(False)
                msg_arr.append("Could not tap savings tile <submit> button")
                take_screenshot(driver, 'submit button')

        driver.tap([(wWidth * 0.75, wHeight * 0.55)]) # tap OK button on pop-up

        # close account

        result_flag_item, msg_item = tap_element(driver, 'savingsAccountTile closeButton')
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'savingsAccountTile closeButton')

        driver.tap([(wWidth * 0.25, wHeight * 0.55)]) # tap CLOSE button on pop-up

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)
        
        verify_test(driver, 'Open Savings Account', 98,  TileDict_reverse[_selector] + ": open a savings account", result_flag, msg)

        pass


def refer_friend_from_contacts(driver, _selector):

        result_flag = True
        msg = "Successfully refer friend from contacts"

        result_flag_arr = []
        msg_arr = []

        try:

                result_flag_item, msg_item = tap_element(driver, 'referFriendTile referFriendButton') # tap CTA
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'referFriendTile referFriendButton')

                result_flag_item, msg_item = tap_list_item(driver, 1) # tap first contact from list
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'list item')

                result_flag_item, msg_item = tap_element(driver, 'Done') # tap picker done button
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'Done')

                result_flag_item, msg_item = tap_element(driver, 'referFriendsTile inviteButton') # tap invite button
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'referFriendsTile inviteButton')

                result_flag_item, msg_item = tap_element(driver, 'referFriendTile referFriendButton') # tap done button to confirm
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'referFriendTile referFriendButton')
        except:
                result_flag = False
                msg = "Could not refer friend from contacts"
                take_screenshot(driver, _selector)

        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)
        
        verify_test(driver, _selector, 103 , TileDict_reverse[_selector] + ": refer friend from contacts", result_flag, msg)

        
        pass


def refer_friend_enter_number(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully referred friend by manual entry"

        result_flag_arr = []
        msg_arr = []

        try:

                result_flag_item, msg_item = tap_element(driver, 'referFriendTile enterPhoneNumberButton') # tap CTA
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'referFriendTile enterPhoneNumberButton')

                result_flag_item, msg_item = tap_element(driver, '5')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '0')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '5')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '9')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '2')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '0')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '2')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '0')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '1')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, '6')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'key')

                result_flag_item, msg_item = tap_element(driver, 'Done')
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'Done')

                result_flag_item, msg_item = tap_element(driver, 'referFriendTile referFriendButton') # tap <invite> button
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'referFriendTile referFriendButton')

                result_flag_item, msg_item = tap_element(driver, 'referFriendTile referFriendButton') # tap <done> button to confirm
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        take_screenshot(driver, 'referFriendTile referFriendButton')


        except:
                result_flag = False
                msg = "Could not refer friend by manual entry"
                take_screenshot(driver, _selector)

        
        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)
        
        verify_test(driver, _selector, 104 , TileDict_reverse[_selector] + ": refer friend by manual entry", result_flag, msg)
        
        pass


def scroll_to_tile(driver, _selector):

        global sDuration

        msg = "Could not scroll to tile: " +  TileDict_reverse[_selector]
        result_flag = False

        if (_selector == "Credit Cards:" or _selector == "You Can Do Better!" or _selector == "Credit Score:"):
                scroll_by_predicate(driver, _selector)

        else:
                wSize = driver.get_window_size("current")
                wWidth = int(wSize["width"])
                wHeight = int(wSize["height"])
                scrollFrom = wHeight * 0.75
                scrollTo = wHeight * 0.25
                offset = wHeight * 0.07

                scrollToFlag= 0
                        
                while(scrollToFlag == 0):
                        
                        try:

                                tile = driver.find_element_by_name(_selector)
                                tileHeight = int(tile.size['height'])
                                upperLeft_y = int(tile.location['y'])
                                lowerLeft_y = upperLeft_y + tileHeight
                                screenHeight = wHeight - offset

                                if (upperLeft_y == 0):
                                        driver.execute_script("mobile: scroll", {"direction":'down'})
                                elif(upperLeft_y > 0 and lowerLeft_y <= screenHeight):
                                        scrollToFlag = 1
                                        result_flag = True
                                        msg = "Msg: Successfully scrolled to tile: " + TileDict_reverse[_selector]
                                        take_screenshot(driver, _selector)
                                        verify_test(driver, _selector, TestrailMap[_selector], TileDict_reverse[_selector], result_flag, msg)
                                else:
                                        driver.swipe(int(wWidth/5), scrollFrom, int(wWidth/5), -(scrollTo), sDuration)
                                        time.sleep(1)
                        except:
                                driver.execute_script("mobile: scroll", {"direction":'down'})

        if (result_flag == False):
                take_screenshot(driver, _selector)

        pass

def scroll_by_predicate(driver, _selector):

        global sDuration

        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])
        scrollFrom = wHeight * 0.75
        scrollTo = wHeight * 0.25
        offset = wHeight * 0.07

        msg = "Could not scroll to tile: " +  TileDict_reverse[_selector]
        result_flag = False
        scrollToFlag= 0

        predicate = 'label CONTAINS' + " \"" + _selector + "\" "
                
        while(scrollToFlag == 0):
                
                try:

                        tile = driver.find_element_by_ios_predicate(predicate)
                        tileHeight = int(tile.size['height'])
                        upperLeft_y = int(tile.location['y'])
                        lowerLeft_y = upperLeft_y + tileHeight
                        screenHeight = wHeight - offset

                        if (upperLeft_y == 0):
                                driver.execute_script("mobile: scroll", {"direction":'down'})
                        elif(upperLeft_y > 0 and lowerLeft_y <= screenHeight):
                                scrollToFlag = 1
                                result_flag = True
                                msg = "Msg: Successfully scrolled to tile: " + TileDict_reverse[_selector]
                                take_screenshot(driver, _selector)
                                verify_test(driver, _selector, TestrailMap[_selector], TileDict_reverse[_selector], result_flag, msg)
                        else:
                                driver.swipe(int(wWidth/5), scrollFrom, int(wWidth/5), -(scrollTo), sDuration)
                                time.sleep(1)
                except:
                        driver.execute_script("mobile: scroll", {"direction":'down'})

        if (result_flag == False):
                take_screenshot(driver, _selector)
        pass


def scroll_to_element(driver, _name):

        wSize = driver.get_window_size("current")
        wWidth = wSize["width"]
        wHeight = wSize["height"]
        scrollFrom = int(wHeight/2)
        scrollTo = int(wHeight/4)
        offset = int(scrollFrom - scrollTo + 10)

        scrollToFlag = 0

        while(scrollToFlag == 0):

                try:

                        _element = driver.find_element_by_name(_name)
                        _element_y = int(_element.location['y'])

                        if (_element_y == 0):
                                driver.execute_script("mobile: scroll", {"direction":'down'})

                        elif(_element_y >= offset):
                                swipe(int(wWidth/5), scrollFrom, int(wWidth/5), -(scrollTo), sDuration)
                                _element_y = _element_y - offset
                                time.sleep(1)
                        else:
                                scrollToFlag = 1
                                _element.click()
                except:
                        driver.execute_script("mobile: scroll", {"direction":'down'})
        
                if (scrollToFlag == 0):
                        print ("ERROR: Could not locate an element")

        pass



def scroll_down(driver):

        global sDuration
        wSize = driver.get_window_size("current")
        wWidth = wSize["width"]
        wHeight = wSize["height"]

        driver.swipe(int(wWidth * 0.25), int(wHeight * 0.50) , int(wWidth * 0.25), int(-(wHeight * 0.25)), sDuration)
        time.sleep(2)

        pass


def scroll_up(driver):

        global sDuration
        wSize = driver.get_window_size("current")
        wWidth = wSize["width"]
        wHeight = wSize["height"]

        driver.swipe(int(wWidth * 0.25), int(wHeight * 0.25) , int(wWidth * 0.25), int(wHeight * 0.50), sDuration)
        time.sleep(2)

        pass


def search_transaction(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully searched a transaction in detail view"

        result_flag_arr = []
        msg_arr = []
        
        try:
                if (driver.find_element_by_ios_predicate('label CONTAINS "Search All" ')):
                        driver.find_element_by_ios_predicate('label CONTAINS "Search All" ').click()
                        _send_keys(driver, "Bite")

                        result_flag_item, msg_item = tap_element(driver, "transaction row")
                        result_flag_arr.append(result_flag_item)
                        msg_arr.append(msg_item)
                        if (result_flag_item == False):
                                take_screenshot(driver, 'transaction row')

                        result_flag_item, msg_item = tap_element(driver, "transaction row")
                        result_flag_arr.append(result_flag_item)
                        msg_arr.append(msg_item)
                        if (result_flag_item == False):
                                take_screenshot(driver, 'transaction row')
        except:
                result_flag_arr.append(False)
                msg_arr.append("Could not type a keyword in the search bar")
                take_screenshot(driver, _selector)


        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        if (result_flag == True):
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 51, TileDict_reverse[_selector] + ": search transaction in detail view", result_flag, msg)


        pass


def search_transaction_2(driver, _selector):

        tap_list_item(driver, 1) # go to 2nd detail view

        driver.find_element_by_ios_predicate('label CONTAINS "Search" ').click()
        _send_keys(driver, "Clarity")
        tap_element(driver, "transaction row")
        tap_element(driver, "transaction row")
        tap_back(driver, 'null') # go back to 1st level detail

        pass 


        '''------------------------------------------------- _SEND_KEYS -----
        |  Function = _SEND_KEYS
        |
        |  Purpose:  
        |
        |  Parameters:
        |      
        |
        |  Returns:  THIS FUNCTION DOES NOT RETURN ANYTHING
        *-------------------------------------------------------------------'''

def _send_keys (driver, keys):
        

        for k in keys:
                if (k.isdigit()):
                        driver.find_element_by_name("more").click()
                        driver.find_element_by_name(k).click()
                        driver.find_element_by_name("more").click()
                elif (k == "_"):
                        driver.find_element_by_name("more").click()
                        driver.find_element_by_name("shift").click()
                        driver.find_element_by_name(k).click()
                        driver.find_element_by_name("more").click()
                else:
                        driver.find_element_by_name(k).click()
        
        pass


def swipe(driver, _selector):

        element_mid_y = (int(find_element(driver, _selector, _selector, _selector).size['height']))/2 + int(find_element(driver, _selector, _selector, _selector).location['y'])

        swipe_left_to_right(driver, element_mid_y)
        swipe_right_to_left(driver, element_mid_y)

        pass

def swipe_upper(driver, _selector):

        wSize = driver.get_window_size('current')
        wHeight = int(wSize['height'])
        flag = 0
        counter = 0
        
        result_flag = True
        msg = "Msg: Successfully swiped horizontally in detail view"


        while(flag == 0 and counter < 4):

                try:
                        if (driver.find_elements_by_class_name('Cell')[0]):
                                scroll_up(driver)
                                swipe_right_to_left(driver, wHeight/4)
                                take_screenshot(driver, "horizontal swipe to left")
                                swipe_left_to_right(driver, wHeight/4)
                                take_screenshot(driver, 'horizontal swipe to right')
                                flag = 1

                except:
                        scroll_up(driver)
                        time.sleep(2)
                        counter += 1


        if (counter == 4):
                result_flag = False
                msg = "Could not swipe horizontally in detail view"
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, 94 , TileDict_reverse[_selector] + ": swipe horizontally in detail view", result_flag, msg)
        
        pass


def swipe_lower(driver, _selector):

        wSize = driver.get_window_size('current')
        wHeight = int(wSize['height'])

        result_flag = True
        msg = "Msg: Successfully swiped horizontally in detail view"

        swipe_right_to_left(driver, wHeight * 0.75)
        take_screenshot(driver, _selector)
        swipe_left_to_right(driver, wHeight * 0.75)
        take_screenshot(driver, _selector)

        verify_test(driver, _selector, 82 , TileDict_reverse[_selector] + ": swipe horizontally in detail view", result_flag, msg)
        
        pass

def swipe_left_to_right(driver, element_mid_y):

        global sDuration
        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])

        driver.swipe(int(wWidth * 0.10), element_mid_y, 2*(int(wWidth)), element_mid_y, sDuration)

        pass


def swipe_right_to_left(driver, element_mid_y):

        global sDuration
        wSize = driver.get_window_size("current")
        wWidth = int(wSize["width"])
        wHeight = int(wSize["height"])

        driver.swipe(int(wWidth * 0.80), element_mid_y, -(int(wWidth)), element_mid_y, sDuration)

        pass

        

'''------------------------------------------------- TAKE_SCREENSHOT -------
        |  Function GET_NEXT_PHOTO_PATH
        |
        |  Purpose:  
        |
        |  Parameters:
        |      
        |
        |  Returns:  THIS FUNCTION RETURNS A DIRECTORY PATH TO WHERE A SCREENSHOT IS SAVED.
        *-------------------------------------------------------------------'''

def take_screenshot(driver, _name):

        global photoNum

        photoNum = photoNum + 1
        fileName = _name + str(photoNum) + '.png'
        
        driver.save_screenshot('./screenshots/' + fileName)

        with open(os.path.join(iosConfig.path, iosConfig.report), 'a') as f:
            f.write("See Screenshot:" + fileName + "\n")

        return 

        pass


def tap_amount_pill(driver, _selector):
        
        result_flag = True
        msg = "Msg: Successfully editted amount pill"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver, "savingsAccountTile amountButton")
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'savingsAccountTile amountButton')
        
        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'picker_done')

        for i in range (0,1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        return result_flag, msg

        pass


def tap_frequency_pill(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully editted frequency pill"

        result_flag_arr = []
        msg_arr = []

        result_flag_item, msg_item = tap_element(driver, "savingsAccountTile frequencyButton")
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'savingsAccountTile frequencyButton')

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'picker_done')

        for i in range (0,1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        return result_flag, msg

        pass


def tap_goal_pill(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully editted goal pill"

        result_flag_arr = []
        msg_arr = []


        result_flag_item, msg_item = tap_element(driver, "savingsAccountTile typeButton")
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'savingsAccountTile typeButton')

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'picker_done')


        for i in range (0,1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        return result_flag, msg

        pass

def tap_account_pill(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully editted account pill"

        result_flag_arr = []
        msg_arr = []

        
        result_flag_item, msg_item = tap_element(driver, "savingsAccountTile pickAccountButton")
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'savingsAccountTile pickAccountButton')

        result_flag_item, msg_item = tap_element(driver, Elements['picker_done'])
        result_flag_arr.append(result_flag_item)
        msg_arr.append(msg_item)
        if (result_flag_item == False):
                take_screenshot(driver, 'picker_done')

        for i in range (0,1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break

        return result_flag, msg

        # to do: tap cta button and then confirm/cancel in the pop-up

        pass


def tap_element(driver, _selector):

        _found, _element = find_element(driver, _selector)
        _found_c, _element_c = find_element_by_class(driver, _selector)
        msg = "null"
        
        if (_found):
                _element.click()
                msg = "Msg: Tapped element with selector: " + _selector
                return _found, msg
        elif(_found_c):
                _element_c.click()
                msg = "Msg: Tapped element with selector: " + _selector
                return _found_c, msg
        else:
                msg = "Couldn't tap element with selector: " + _selector
                return False, msg

        pass

def tap_element_by_predicate(driver, _selector):

        _found, _element = find_element_by_predicate(driver, _selector)
        
        if (_found == True ):
                _element.click()
                return True, "Tapped selector" + _selector
        else:
                return False, "Couldn't tap selector " + _selector

        pass


def tap_back(driver, _selector):

        global maxWait

        result_flag = False
        msg = "Could not tap " + TileDict_reverse[_selector] + " back button in detail view"

        for x in range (0, maxWait):
                
                try:
                        
                        if (driver.find_element_by_ios_predicate('value == "Back"')):
                                driver.find_element_by_ios_predicate('value == "Back"').click()
                                result_flag = True
                                msg = "Msg: Successfully tapped " + TileDict_reverse[_selector] + " back button in detail view"
                                time.sleep(1)
                                take_screenshot(driver, _selector)
                                break
                                
                except:
                        if (x + 1 == maxWait):
                                take_screenshot(driver, _selector + " back button")
                                break

                        time.sleep(1)
        
        
        verify_test(driver, _selector, TestrailMap_backButton[_selector], (TileDict_reverse[_selector] + ": tap back button in detail view"), result_flag, msg)

        pass


def tap_back_2 (driver):

        global maxWait

        for x in range (0, maxWait):
                
                try:
                        
                        if (driver.find_element_by_ios_predicate('value == "Back"')):
                                driver.find_element_by_ios_predicate('value == "Back"').click()
                                break
                                
                except:
                        if (x + 1 == maxWait):
                                break

                        time.sleep(1)
        pass


def tap_tile(driver, _selector):

        if (_selector == "Credit Cards:" or _selector == "You Can Do Better!" or _selector == "Credit Score:"):
                result_flag, msg = tap_tile_by_predicate(driver, _selector)
                time.sleep(1)
                take_screenshot(driver, _selector)
                verify_test(driver, _selector, TestrailMap_detailView[_selector], TileDict_detail_reverse[_selector], result_flag, msg)

        else:
                result_flag, msg = tap_element(driver, _selector)
                time.sleep(1)
                take_screenshot(driver, _selector)
                verify_test(driver, _selector, TestrailMap_detailView[_selector], TileDict_detail_reverse[_selector], result_flag, msg)

        pass

def tap_tile_by_predicate(driver, _selector):

        result_flag, msg = tap_element_by_predicate(driver, _selector)

        return result_flag, msg

        pass


def tap_cta(driver, _selector):

        tap_element(driver, 'Button')
        tap_back_2(driver) # go back to detail view

        pass

def tap_list_item(driver, itemNum):

        result_flag = True
        msg = "Msg: Successfully tapped list item"

        try:
                driver.find_elements_by_class_name('Cell')[itemNum].click()
                time.sleep(2)
        except:
                result_flag = False
                msg = "Could not tap list item"

        return result_flag, msg

        pass

def toggle_recurrence(driver, _selector):

        result_flag = True
        msg = "Msg: Successfully toggled recurrence"

        result_flag_arr = []
        msg_arr = []

        try:

                result_flag_item, msg_item = tap_element(driver, Elements['cell'])
                result_flag_arr.append(result_flag_item)
                msg_arr.append(msg_item)
                if (result_flag_item == False):
                        time.sleep(1)
                        take_screenshot(driver, 'cell')

                try:
                        if (driver.find_element_by_class_name(Elements['switch'])):

                                scroll_down(driver)
                                driver.find_element_by_class_name(Elements['switch']).click()
                                
                                result_flag_item, msg_item = tap_element(driver, Elements['cell'])
                                result_flag_arr.append(result_flag_item)
                                msg_arr.append(msg_item)
                                if (result_flag_item == False):
                                        time.sleep(1)
                                        take_screenshot(driver, 'cell')
                                
                        else:
                                result_flag_item = False
                                msg_item = "Unable to find/click toggle swtich"
                                result_flag_arr.append(result_flag_item)
                                msg_arr.append(msg_item)
                                time.sleep(1)
                                take_screenshot(driver, _selector)
                except:
                        scroll_down(driver)

        except:
                scroll_to_element(driver, Elements['cell'])

        
        for i in range (0, len(result_flag_arr)-1):
                if (result_flag_arr[i] == False):
                        result_flag = result_flag_arr[i]
                        msg = msg_arr[i]
                        break
                
        if (result_flag == True):
                time.sleep(1)
                take_screenshot(driver, _selector)

        verify_test(driver, _selector, TestrailMap_toggleRecurrence[_selector], TileDict_reverse[_selector] + ": toggle recurrence in detail view", result_flag, msg)

        pass

def toggle_recurrence_list_item(driver, _selector):

        tap_list_item(driver, 1) # expand a list item
        driver.find_element_by_class_name(Elements['switch']).click() # toggle recurrence

        pass


def toggle_recurrence_2(driver, _selector):

        tap_list_item(driver, 1) # go to 2nd detail view

        try:
                tap_element(driver, Elements['cell'])

                try:
                        if (driver.find_element_by_class_name(Elements['switch'])):
                                scroll_down(driver)
                                driver.find_element_by_class_name(Elements['switch']).click()
                                tap_element(driver, Elements['cell'])
                                tap_back_2(driver) # go back to 1st level detail
                except:
                        scroll_down(driver)

        except:
                scroll_to_element(driver, Elements['cell'])

        pass


def toggle_view(driver,_selector):

        flag = 0
        counter = 0

        result_flag = True
        msg = "Msg: Successfully toggled view"

        result_flag_arr = []
        msg_arr = []


        while(flag == 0 and counter < 4):

                try:
                        if (driver.find_element_by_ios_predicate('value == "Graph" ')):
                                driver.find_element_by_ios_predicate('value == "Graph" ').click()
                                time.sleep(1)
                                take_screenshot(driver, 'Graph icon')
                                driver.find_element_by_ios_predicate('value == "Pie Chart" ').click()
                                time.sleep(1)
                                take_screenshot(driver, 'Pie Chart icon')
                                flag = 1

                        elif(driver.find_element_by_ios_predicate('value == "Pie Chart" ')):
                                driver.find_element_by_ios_predicate('value == "Pie Chart" ').click()
                                time.sleep(1)
                                take_screenshot(driver, 'Pie Chart icon')
                                driver.find_element_by_ios_predicate('value == "Graph" ').click()
                                time.sleep(1)
                                take_screenshot(driver, 'Graph icon')
                                flag = 1

                except:
                        scroll_up(driver)
                        time.sleep(2)
                        counter += 1
                
        if (counter == 4):
                result_flag = False
                msg = "Could not toggle view"
                time.sleep(1)
                take_screenshot(driver, _selector)


        verify_test(driver, _selector, 59 , TileDict_reverse[_selector] + ": toggle view in detail view", result_flag, msg)


        pass



def updateTestrailTestRun(project_name, testRun_name, case_id, case_name, result_flag):
        
        test_run_id = testrail_integration.get_run_id(testRun_name,project_name)

        if (result_flag):
                msg = "PASSED: " + case_name
        else:
                msg = "FAILED: " + case_name

        testrail_integration.update_testrail(case_id,test_run_id, result_flag, msg=msg)

        pass



def verify_test(driver, _selector, _case_id, _case_name, _result_flag, msg):

        global maxWait

        # append test case result and message to report
        if (_result_flag):
                with open(os.path.join(iosConfig.path, iosConfig.report), 'a') as f:
                        result = 'PASSED....: ' + _case_name
                        f.write(result + "\n\n")
        else:
                with open(os.path.join(iosConfig.path, iosConfig.report), 'a') as f:
                        result = 'FAILED....: ' + _case_name
                        f.write(result + "\n")
                        f.write("Msg: " + msg + "\n\n")

        # append screenshot to report
        #take_screenshot(driver, _selector)

        # update testrail
        updateTestrailTestRun(iosConfig.getProjectName(),iosConfig.getTestRun(), _case_id, _case_name, _result_flag)

        pass 


def updateTestrailTestRun(project_name, testRun_name, case_id, case_name, result_flag):  

        test_run_id = testrail_integration.get_run_id(testRun_name,project_name)

        
        if (result_flag):
            msg = "PASSED: " + case_name
        else:
            msg = "FAILED: " + case_name
        

        testrail_integration.update_testrail(case_id,test_run_id,result_flag, msg=msg)

        pass



# tile dictionary

TileDict = {
        
        'Balance': 'Cash',
        'Daily Summary': 'daily summary tile',
        'Transactions': 'transaction row',
        'CreditCardDue': 'creditCardDueTile',
        'IncomeThisMonth': 'incomeThisMonthTile',
        'MonthlyIncome': 'monthlyIncomeTile',
        'CategorySpending': 'categorySpendingTile',
        'CancelSubscription': 'subscriptionTakeALookButton',
        'WhatDidISpend': 'whatDidISpendTile takeALookButton',
        'Transfer': 'transfersTile DoItButton',
        'CreditScore': 'Credit Score:',
        'Notifications': 'notificationsTile',
        'LowerBills': 'lowerBillsTile checkItOutButton',
        'CreditCards': 'Credit Cards:',
        'DoBetter': 'You Can Do Better!',
        'Savings': 'savingsAccountTile doItButton',
        'ReferFriend': 'referFriendTile referFriendButton',
        'HowItWorks': 'howItWorksTile',
        'ThankYou': 'thankYouTile'
        
}


TileDict_reverse = {

        'Cash': 'Balance',
        'daily summary tile': 'Daily Summary',
        'transaction row': 'Transactions',
        'creditCardDueTile': 'CreditCardDue',
        'incomeThisMonthTile': 'IncomeThisMonth',
        'monthlyIncomeTile': 'MonthlyIncome',
        'categorySpendingTile': 'CategorySpending',
        'subscriptionTakeALookButton': 'CancelSubscription',
        'whatDidISpendTile takeALookButton': 'WhatDidISpend',
        'transfersTile DoItButton': 'Transfer',
        'Credit Score:': 'CreditScore',
        'notificationsTile': 'Notifications',
        'lowerBillsTile checkItOutButton': 'LowerBills',
        'Credit Cards:':  'CreditCards',
        'You Can Do Better!': 'DoBetter',
        'savingsAccountTile doItButton': 'Savings',
        'referFriendTile referFriendButton': 'ReferFriend',
        'howItWorksTile': 'HowItWorks',
        'thankYouTile': 'ThankYou'

}


TileDict_detail_reverse = {

        'Cash': 'Balance Tile Detail View',
        'daily summary tile': 'Daily Summary Tile Detail View',
        'transaction row': 'Transactions Tile Detail View',
        #'creditCardDueTile': 'CreditCardDue',
        'incomeThisMonthTile': 'IncomeThisMonth Tile Detail View',
        'monthlyIncomeTile': 'MonthlyIncome Tile Detail View',
        'categorySpendingTile': 'CategorySpending Tile Detail View',
        'subscriptionTakeALookButton': 'CancelSubscription Tile Detail View',
        'whatDidISpendTile takeALookButton': 'WhatDidISpend Tile Detail View',
        'transfersTile DoItButton': 'Transfer Tile Detail View',
        'Credit Score:': 'CreditScore Tile Detail View',
        #'notificationsTile': 'Notifications',
        'lowerBillsTile checkItOutButton': 'LowerBills Tile Detail View',
        'Credit Cards:':  'CreditCards Tile Detail View',
        #'You Can Do Better!': 'DoBetter',
        'savingsAccountTile doItButton': 'Savings Tile Detail View',
        'referFriendTile referFriendButton': 'ReferFriend Tile Detail View',
        #'howItWorksTile': 'HowItWorks',
        'thankYouTile': 'ThankYou Tile Detail View'
}


# mapping from tile to testrail case id        

TestrailMap = {

        'Cash': '3', # balance tile
        'daily summary tile': '4', # daily summary tile
        'transaction row': '20', # transactions tile
        'creditCardDueTile': '21', # credit card due tile
        'incomeThisMonthTile': '22', # income this month tile
        'monthlyIncomeTile': '23', # monthly income tile
        'categorySpendingTile': '24', # category spending tile
        'subscriptionTakeALookButton': '25' , # cancel subscription tile
        'whatDidISpendTile takeALookButton': '26', # what did I spend tile
        'transfersTile DoItButton': '27', # transfer tile
        'Credit Score:': '28', # credit score tile
        'notificationsTile': '34', # notifications tile
        'lowerBillsTile checkItOutButton': '29', # lower bills tile
        'Credit Cards:': '30', # credit cards tile
        'You Can Do Better!': '31', # do better tile
        'savingsAccountTile doItButton': '32', # savings tile
        'referFriendTile referFriendButton': '33', # refer friend tile
        'howItWorksTile': '35', # how it works tile
        'thankYouTile': '36' # thank you tile

}


TestrailMap_detailView = {

        'Cash': '110', # balance tile detail view
        'daily summary tile': '111', # daily summary tile detail view
        'transaction row': '112', # transactions tile detail view
        #'creditCardDueTile': '', # credit card due tile detail view
        'incomeThisMonthTile': '113', # income this month tile detail view
        'monthlyIncomeTile': '114', # monthly income tile detail view
        'categorySpendingTile': '115', # category spending tile detail view
        'subscriptionTakeALookButton': '116' , # cancel subscription tile detail view
        'whatDidISpendTile takeALookButton': '117', # what did I spend tile detail view
        'transfersTile DoItButton': '118', # transfer tile detail view
        'Credit Score:': '119', # credit score tile detail view
        #'notificationsTile': '', # notifications tile detail view
        'lowerBillsTile checkItOutButton': '120', # lower bills tile detail view
        'Credit Cards:': '121', # credit cards tile detail view
        #'You Can Do Better!': '', # do better tile detail view
        'savingsAccountTile doItButton': '122', # savings tile detail view
        'referFriendTile referFriendButton': '123', # refer friend tile detail view
        #'howItWorksTile': '', # how it works tile detail view
        'thankYouTile': '124' # thank you tile detail view

}


TestrailMap_backButton = {

        'Cash': '42', # balance tile back button
        'daily summary tile': '45', # daily summary tile back button
        'transaction row': '52', # transactions tile back button
        #'creditCardDueTile': '', # static tile
        'incomeThisMonthTile': '56', # income this month tile back button
        'monthlyIncomeTile': '61', # monthly income tile back button
        'categorySpendingTile': '68', # category spending tile back button
        'subscriptionTakeALookButton': '72' , # cancel subscription tile back button
        'whatDidISpendTile takeALookButton': '77', # what did I spend tile back button
        'transfersTile DoItButton': '81', # transfer tile back button
        'Credit Score:': '83', # credit score tile back button
        #'notificationsTile': '', # static tile
        'lowerBillsTile checkItOutButton': '88', # lower bills tile back button
        'Credit Cards:': '95', # credit cards tile back button
        #'You Can Do Better!': '', # static tile
        'savingsAccountTile doItButton': '99', # savings tile back button
        'referFriendTile referFriendButton': '105', # refer friend tile back button
        #'howItWorksTile': '', # static tile
        'thankYouTile': '109' # thank you tile back button

}                          


TestrailMap_editCategory = {

        'daily summary tile': '43',
        'transaction row': '47', 
        'incomeThisMonthTile': '55', 
        'monthlyIncomeTile': '57', 
        'categorySpendingTile': '65', 
        'whatDidISpendTile takeALookButton': '73', 
        'Credit Cards:': '91'
}


TestrailMap_toggleRecurrence = {

        'daily summary tile': '44',
        'transaction row': '48',
        'monthlyIncomeTile': '58',
        'categorySpendingTile': '66',
        'whatDidISpendTile takeALookButton': '74',
        'Credit Cards:': '92'
}


TestrailMap_editOrder = {

        'transaction row': '46',
        'Credit Cards:': '90'
}

TestrailMap_editTransFilter = {

        'transaction row': '50',
        'Credit Cards:': '93'
}


# mapping of tiles to actions

ActionMap = {

        #'Balance': [7,8,9,10,11,26], # to-do: 2nd level actions
        'Balance': [26, 27],
        'Daily Summary': [3,4,27],
        'Transactions': [1, 2, 3, 4, 6, 27],
        'CreditCardDue': [27],
        'IncomeThisMonth': [3, 27],
        'MonthlyIncome': [3,4,12, 27],
        'CategorySpending': [0, 3, 4, 5, 27],
        'CancelSubscription': [34, 27],
        'WhatDidISpend': [3,4,14,15,27],
        'Transfer': [16, 27],
        'CreditScore': [20,27],
        'Notifications': [27],
        'LowerBills': [29, 27],
        'CreditCards': [1,3,4,6,19,27],
        'DoBetter': [27],
        'Savings': [31,27],
        'ReferFriend': [32,33, 27],
        'HowItWorks': [27],
        'ThankYou': [26, 27]
}

# action dictionary

ActionDict = {

        '0': edit_category_filter, # done
        '1': edit_order, # done
        '2': search_transaction, # done
        '3': edit_category, # done
        '4': toggle_recurrence, # done
        '5': loop_category, # done
        '6': edit_transaction_filter, # done
        '7': edit_transaction_filter_2, # skip
        '8': edit_order_2, # skip
        '9': edit_category_2, # skip
        '10': toggle_recurrence_2, # skip
        '11': search_transaction_2, # skip
        '12': toggle_view, # done
        '13': tap_cta, #skip
        '14': edit_vendor_pill, # done
        '15': edit_filter_pill, # done
        '16': transfer_money, # done
        '17': dismiss_tile_darkX, # skip
        '18': dismiss_tile_lightX, # skip
        '19': swipe_upper, # done
        '20': swipe_lower, # done
        '21': swipe, #skip for now
        '22': tap_amount_pill, # done 
        '23': tap_frequency_pill, # done
        '24': tap_goal_pill, # done
        '25': tap_account_pill, # done
        '26': tap_back, #done
        '27': do_nothing, # done
        '28': toggle_recurrence_list_item, # skip
        '29': lower_bill, # done
        '30': do_better, # skip
        '31': open_close_savings, # done
        '32': refer_friend_from_contacts, # done
        '33': refer_friend_enter_number, # done
        '34': cancel_subscription # done
}  

# end of file                                       