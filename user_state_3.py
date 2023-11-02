#!/usr/bin/python
# -*- coding: utf-8 -*-
import pgdb
from datetime import datetime, timedelta, date

print "Using PyGreSQL…"
hostname = 'clarity-dev-5.csb0csrt2o42.us-east-1.rds.amazonaws.com'
username = 'clarity'
password = '6mtrSua8'
database = 'clarity'


#
# create savings account with no saved money
#

def create_savings(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT id FROM account WHERE user_id = %s AND deleted_at IS NULL AND sub_type = 'checking'" % userId
    cur.execute( q0 )
    accountId = str(cur.fetchone()[0])

    # to-do : check to make sure user does not already have a savings account

    q1 = "INSERT INTO auto_deposit (account_id, user_id, amount, description, created_at, updated_at, is_active, last_processed, frequency, day_of_month, day_of_week, account_closure_initiated_at, deleted_at, return_count, previous_auto_deposit_id, display_account_id) VALUES(%s, %s, 15.00, 'car', NOW(), NOW() ,TRUE, NULL, 'WEEKLY', NULL, 1, NULL, NULL, 0, NULL, NULL)" % (accountId, userId)
    cur.execute( q1 )
    myConnection.commit()

    q2 = "SELECT max(id) FROM auto_deposit"
    cur.execute( q2 )
    maxId_auto_deposit = str(cur.fetchone()[0])

    q3 = "INSERT INTO cmsa_deposit_rule (auto_deposit_id, rule_meta, last_processed, amount, created_at, updated_at, deleted_at, rule_type) VALUES(%s, '{\"day\":1}', NULL, 15.00, NOW(), NOW(), NULL, 'WEEKLY')" % maxId_auto_deposit
    cur.execute( q3 )
    myConnection.commit()

    print "Savings account created for user id: %s" % userId

    myConnection.close()

#
# close savings account with no saved money
#

def close_savings(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # to-do : check to make sure user already has a savings account

    q0 = "SELECT id FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    auto_deposit_id = str(cur.fetchone()[0])

    q1= "UPDATE auto_deposit SET account_closure_initiated_at = 'NOW()', deleted_at = 'NOW()' WHERE user_id = %s" % userId
    cur.execute( q1 )
    myConnection.commit()

    q2 = "UPDATE cmsa_deposit_rule SET deleted_at = 'NOW()' WHERE auto_deposit_id = %s" % auto_deposit_id
    cur.execute( q2 )
    myConnection.commit()

    myConnection.close()


#
# create savings account with saved money (active)
#

def bonus_with_savings(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    create_savings(userId)

    q0 = "SELECT account_id FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    accountId = str(cur.fetchone()[0])

    q1 = "INSERT INTO user_bonus (user_id, amount, reason, created_at, updated_at, clarity_account_id, account_id, paid_at, user_referral_id, reclaimed_date, is_covered) VALUES (%s, 6.00, 'user state automation', NOW(), NOW(), 1, %s, NOW(), NULL, NULL, TRUE)" % (userId, accountId)
    cur.execute(q1)
    myConnection.commit()

    q2 = "SELECT max(id) FROM user_bonus"
    cur.execute(q2)
    max_user_bonus_id = str(cur.fetchone()[0])

    q3 = "INSERT INTO cash_ledger (account_id, fbo_institution_id, type, stage, amount, created_at, updated_at, ach_transaction_id, effective_date, clarity_account_id, user_bonus_id) VALUES (%s, 1, 'CREDIT', 'CLARITY_BONUS', -6.00, NOW(), NOW(), NULL, NOW(), NULL, %s)" % (accountId, max_user_bonus_id)
    cur.execute( q3 )
    myConnection.commit()

    myConnection.close()

    print "User %s received bonus" % userId


#
# create savings account with saved money (paused)
#

def bonus_with_savings_paused(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    create_savings(userId)

    q0 = "SELECT account_id FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    accountId = str(cur.fetchone()[0])

    q1 = "INSERT INTO user_bonus (user_id, amount, reason, created_at, updated_at, clarity_account_id, account_id, paid_at, user_referral_id, reclaimed_date, is_covered) VALUES (%s, 111.00, 'user state automation', NOW(), NOW(), 1, %s, NOW(), NULL, NULL, TRUE)" % (userId, accountId)
    cur.execute(q1)
    myConnection.commit()

    q2 = "SELECT max(id) FROM user_bonus"
    cur.execute(q2)
    max_user_bonus_id = str(cur.fetchone()[0])

    q3 = "INSERT INTO cash_ledger (account_id, fbo_institution_id, type, stage, amount, created_at, updated_at, ach_transaction_id, effective_date, clarity_account_id, user_bonus_id) VALUES (%s, 1, 'CREDIT', 'CLARITY_BONUS', -111.00, NOW(), NOW(), NULL, NOW(), NULL, %s)" % (accountId, max_user_bonus_id)
    cur.execute( q3 )
    myConnection.commit()

    q4 = "UPDATE auto_deposit SET is_active = FALSE WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q4 )
    myConnection.commit()

    myConnection.close()

    print "User %s received bonus and account is paused" % userId


def savings_paused(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    create_savings(userId)

    q0 = "UPDATE auto_deposit SET is_active = FALSE WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    myConnection.commit()

    myConnection.close()

    print "User %s account is paused" % userId

#
# assign bonus to a user with no savings account
#

def bonus_without_savings(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "INSERT INTO user_bonus (user_id, amount, reason, created_at, updated_at, clarity_account_id, account_id, paid_at, user_referral_id, reclaimed_date, is_covered) VALUES (%s, 111.00, 'user state automation', NOW(), NOW(), NULL, NULL, NULL, NULL, NULL, TRUE)" % userId
    cur.execute(q0)
    myConnection.commit()

    myConnection.close()

    print "Assigned bonus process takes about 20 minutes. Please check savings tile for user %s 20 minutes later." % userId


#
# reset savings tile to its initial state
#

def reset_savings_tile (userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # step 1: undo bonus assignment

    q14 = "SELECT COUNT(*) FROM user_bonus WHERE user_id = %s" % userId
    cur.execute( q14 )
    result14 = str(cur.fetchone()[0])
    
    if (int(result14) == 0):
        print ''
    else:
        q9 = "SELECT max(id) FROM user_bonus WHERE user_id = %s" % userId
        user_bonus_id = cur.execute( q9 ).fetchone()

        q10 = "DELETE FROM cash_ledger WHERE user_bonus_id = %s" % user_bonus_id
        cur.execute( q10 )
        myConnection.commit()

        q11 = "DELETE FROM user_bonus WHERE id = %s" % user_bonus_id
        cur.execute( q11 )
        myConnection.commit()

    # step 2: undo savings creation

    # 2(a) delete CLARITY BONUS from cash_ledger

    q5 = "SELECT id FROM account WHERE user_id = %s AND name = 'Clarity Savings'" % userId
    Clarity_account_id = cur.execute( q5 ).fetchone() # account id when user is assigned bonus

    if (Clarity_account_id is not None):
        q6 = "DELETE FROM cash_ledger WHERE account_id = %s" % Clarity_account_id
        cur.execute( q6 )
        myConnection.commit()

        q7 = "UPDATE account SET deleted_at = 'NOW()' WHERE user_id = %s AND name = 'Clarity Savings' " % userId
        cur.execute( q7 )
        myConnection.commit()

        q1 = "SELECT account_id FROM auto_deposit WHERE user_id = %s AND description = 'Bonus Withdrawal'" % userId
        bonus_withdrawal_account_id = cur.execute( q1 ).fetchone() # account id when user withdraws bonus

        if (bonus_withdrawal_account_id is not None):
            q8 = "DELETE FROM cash_ledger WHERE account_id = %s" % bonus_withdrawal_account_id
            cur.execute( q8 )
            myConnection.commit()

    # 2(b) delete HANDOFF from cash_ledger

        q12 = "DELETE FROM cash_ledger WHERE stage = 'BONUS_HANDOFF' AND account_id = %s " % Clarity_account_id
        cur.execute( q12 )
        myConnection.commit()

        if (bonus_withdrawal_account_id is not None):
            q13 = "DELETE FROM cash_ledger WHERE stage = 'BONUS_HANDOFF' AND account_id = %s " % bonus_withdrawal_account_id
            cur.execute( q13 )
            myConnection.commit()

    q0 = "SELECT max(id) FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    auto_deposit_id = cur.execute( q0 ).fetchone()

    q3 = "UPDATE auto_deposit SET account_closure_initiated_at = 'NOW()', deleted_at = 'NOW()' WHERE deleted_at IS NULL AND user_id = %s" % userId
    cur.execute( q3 )
    myConnection.commit()

    q2 = "UPDATE ach_transaction SET is_failed = TRUE, is_pending = FALSE WHERE auto_deposit_id = %s" % auto_deposit_id
    cur.execute( q2 )
    myConnection.commit() 

    q4 = "UPDATE cmsa_deposit_rule SET deleted_at = 'NOW()' WHERE auto_deposit_id = %s" % auto_deposit_id
    cur.execute( q4 )
    myConnection.commit()

    myConnection.close()

    print "Savings tile is reset for user %s" % userId


#
# success state
#
def savings_passKyc_passTerms(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # pass kyc

    q0 = "SELECT COUNT(*) FROM user_kyc_result WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) != 0):
        q1 = "UPDATE user_kyc_result SET has_passed_check = TRUE WHERE user_id = %s AND deleted_at IS NULL" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:
        q2 = "INSERT INTO user_kyc_result (user_id, has_passed_check, dob, first_name, last_name, address_1, address_2, city, state, zip, ssn, created_at, updated_at) VALUES (%s, TRUE, '1991-01-24', 'Clarity', 'Money', '28 Gates Ave', 'A', 'Summit', 'NJ', 07901,'AQICAHi0dYssjGm5mzT4ni95v1B2HcwuzVFw+bbL/wEIVMPyowFGxseMdeuZIe3wpWSUppkoAAAAZzBlBgkqhkiG9w0BBwagWDBWAgEAMFEGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMVHQmT09EWTAV8D20AgEQgCQNjvLglU9qcdkm3NXudZyRwEtbrOBC7E68REDf3TP9z+Gy8FQ=', NOW(), NOW())" % userId
        cur.execute( q2 )
        myConnection.commit()

    # pass terms

    q3 = "SELECT COUNT(*) FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q3 )
    result3 = str(cur.fetchone()[0])

    if (int(result3) != 0):
        q4 = "UPDATE auto_deposit SET accepted_terms_at = NOW() WHERE deleted_at IS NULL AND user_id = %s" % userId
        cur.execute( q4 )
        myConnection.commit()

    myConnection.close()

    print "Passed KYC and passed terms for user %s" % userId

#
# don't need full kyc
#

def savings_passKyc_failTerms(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # pass kyc

    q2 = "SELECT COUNT(*) FROM user_kyc_result WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q2 )
    result2 = str(cur.fetchone()[0])

    if (int(result2) != 0):
        q3 = "UPDATE user_kyc_result SET has_passed_check = TRUE WHERE user_id = %s AND deleted_at IS NULL" % userId
        cur.execute( q3 )
        myConnection.commit()
    
    else:
        q4 = "INSERT INTO user_kyc_result (user_id, has_passed_check, dob, first_name, last_name, address_1, address_2, city, state, zip, ssn, created_at, updated_at) VALUES (%s, TRUE, '1991-01-24', 'Clarity', 'Money', '28 Gates Ave', 'A', 'Summit', 'NJ', 07901,'AQICAHi0dYssjGm5mzT4ni95v1B2HcwuzVFw+bbL/wEIVMPyowFGxseMdeuZIe3wpWSUppkoAAAAZzBlBgkqhkiG9w0BBwagWDBWAgEAMFEGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMVHQmT09EWTAV8D20AgEQgCQNjvLglU9qcdkm3NXudZyRwEtbrOBC7E68REDf3TP9z+Gy8FQ=', NOW(), NOW())" % userId
        cur.execute( q4 )
        myConnection.commit()

    # fail terms

    q0 = "SELECT COUNT(*) FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) != 0):
        q1 = "UPDATE auto_deposit SET accepted_terms_at = NULL WHERE deleted_at IS NULL AND user_id = %s" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    #else:
        #create_savings(userId)

        #q5 = "UPDATE auto_deposit SET accepted_terms_at = NULL WHERE deleted_at IS NULL AND user_id = %s" % userId
        #cur.execute( q5 )
        #myConnection.commit()

    myConnection.close()

    print "Passed KYC and failed terms for user %s" % userId

#
# Failed state
#

def savings_failKyc_passTerms(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # fail kyc

    q0 = "SELECT COUNT(*) FROM user_kyc_result WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) != 0):
        q1 = "UPDATE user_kyc_result SET has_passed_check = FALSE WHERE user_id = %s AND deleted_at IS NULL" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:
        q4 = "INSERT INTO user_kyc_result (user_id, has_passed_check, dob, first_name, last_name, address_1, address_2, city, state, zip, ssn, created_at, updated_at) VALUES (%s, FALSE, '1991-01-24', 'Clarity', 'Money', '28 Gates Ave', 'A', 'Summit', 'NJ', 07901,'AQICAHi0dYssjGm5mzT4ni95v1B2HcwuzVFw+bbL/wEIVMPyowFGxseMdeuZIe3wpWSUppkoAAAAZzBlBgkqhkiG9w0BBwagWDBWAgEAMFEGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMVHQmT09EWTAV8D20AgEQgCQNjvLglU9qcdkm3NXudZyRwEtbrOBC7E68REDf3TP9z+Gy8FQ=', NOW(), NOW())" % userId
        cur.execute( q4 )
        myConnection.commit()

    # pass terms

    q2 = "SELECT COUNT(*) FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q2 )
    result2 = str(cur.fetchone()[0])

    if (int(result2) != 0):
        q3 = "UPDATE auto_deposit SET accepted_terms_at = NOW() WHERE deleted_at IS NULL AND user_id = %s" % userId
        cur.execute( q3 )
        myConnection.commit()
    '''
    else:
        create_savings(userId)

        q4 = "UPDATE auto_deposit SET accepted_terms_at = NOW() WHERE deleted_at IS NULL AND user_id = %s" % userId
        cur.execute( q4 )
        myConnection.commit()
    '''
    myConnection.close()

    print "Failed KYC and passed terms for user %s" % userId

#
# need full kyc
#

def savings_noKyc_failTerms(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # have not received kyc

    q0 = "SELECT COUNT(*) FROM user_kyc_result WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) != 0):
        q1 = "UPDATE user_kyc_result SET deleted_at = NOW() WHERE user_id = %s" % userId
        cur.execute( q1 )
        myConnection.commit()

    '''
    else:
        q4 = "INSERT INTO user_kyc_result (user_id, has_passed_check, dob, first_name, last_name, address_1, address_2, city, state, zip, ssn, created_at, updated_at) VALUES (%s, NULL, '1991-01-24', 'Clarity', 'Money', '28 Gates Ave', 'A', 'Summit', 'NJ', 07901,'AQICAHi0dYssjGm5mzT4ni95v1B2HcwuzVFw+bbL/wEIVMPyowFGxseMdeuZIe3wpWSUppkoAAAAZzBlBgkqhkiG9w0BBwagWDBWAgEAMFEGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMVHQmT09EWTAV8D20AgEQgCQNjvLglU9qcdkm3NXudZyRwEtbrOBC7E68REDf3TP9z+Gy8FQ=', NOW(), NOW())" % userId
        cur.execute( q4 )
        myConnection.commit()
    '''

    # fail terms

    q2 = "SELECT COUNT(*) FROM auto_deposit WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q2 )
    result2 = str(cur.fetchone()[0])

    if (int(result2) != 0):
        q3 = "UPDATE auto_deposit SET accepted_terms_at = NULL WHERE deleted_at IS NULL AND user_id = %s" % userId
        cur.execute( q3 )
        myConnection.commit()
    
    '''
    else:
        create_savings(userId)

        q4 = "UPDATE auto_deposit SET accepted_terms_at = NULL WHERE deleted_at IS NULL AND user_id = %s" % userId
        cur.execute( q4 )
        myConnection.commit()
    '''

    myConnection.close()

    print "No KYC and failed terms for user %s" % userId



def enable_lemonade(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    enable_loans_specific(userId)

    q0 = "UPDATE user_targeting SET show_lemonade = TRUE where user_id = %s " % userId
    cur.execute( q0 )
    myConnection.commit()

    myConnection.close()


def enable_sofi(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    enable_loans_specific(userId)

    q0 = "UPDATE user_targeting SET show_student_loan = TRUE, show_personal_loan = FALSE WHERE user_id = %s " % userId
    cur.execute( q0 )
    myConnection.commit()

    myConnection.close()


#
# this function will make loans tile (with generic message) visible to user, which will turn off credit card offers tile if user has it
#

def enable_loans_generic (userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    # make sure <user_personal_loan> table has record for the user

    q0 = "SELECT COUNT(*) FROM user_personal_loan WHERE user_id = %s" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])
    print "does user have record in <user_personal_loan> table? " + result0

    if (int(result0) == 0):

        q1 = "INSERT INTO user_personal_loan (status, user_id, json, created_at, updated_at, type) VALUES ('offered', %s, '[]', NOW(), NOW(), 'prosper')" % userId
        cur.execute( q1 )
        myConnection.commit()
        print "inserted into <user_personal_loan> table"

    # make sure <user_targeting> table has record for the user

    q2 = "SELECT COUNT(*) FROM user_targeting WHERE user_id = %s" % userId
    cur.execute( q2 )
    result2 = str(cur.fetchone()[0])
    print "does user have record in <user_targeting> table? " + result2

    if (int(result2) == 0):

        q3 = "INSERT INTO user_targeting (user_id, show_acorns, show_personal_loan, created_at, updated_at, is_account_verifiable, show_student_loan) VALUES (%s, TRUE, TRUE, NOW(), NOW(), TRUE, FALSE)" % userId
        cur.execute( q3 )
        myConnection.commit()
        print "inserted into <user_targeting> table"
    else:
        q4 = "UPDATE user_targeting SET loan_savings = 99.00, show_student_loan = FALSE WHERE user_id = %s" % userId
        cur.execute( q4 )
        myConnection.commit()
        print "updated <user_targeting> table"

    # make sure <user_permanent_tile> table has loans tile for the user

    q5 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 28" % userId
    cur.execute( q5 )
    result5 = str(cur.fetchone()[0])
    print "does user have record in <user_permanent_tile> table? " + result5

    if (int(result5) == 0):

        q6 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (28, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q6 )
        myConnection.commit()
        print "inserted into <user_permanent_tile> table"
    else:
        q7 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL WHERE user_id = %s AND permanent_tile_id = 28" % userId
        cur.execute( q7 )
        myConnection.commit()
        print "updated <user_permanent_tile> table"

    myConnection.close()

    print "Loans tile (w/ generic message) is available for user %s" % userId


#
# this function will make loans tile (with specific message) visible to user, which will turn off credit card offers tile if user has it
#

def enable_loans_specific(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    enable_loans_generic(userId)

    q0 = "UPDATE user_personal_loan SET json = '[{\"apr\": 17.89, \"fee\": 300, \"loan_id\": 427524, \"loan_rate\": 14.23, \"loan_amount\": 6000, \"referral_code\": \"F66FE38E-CA67-4908-9DAA-B7D7D9186615\", \"est_monthly_payment\": 205.74, \"loan_term_in_months\": 36}, {\"apr\": 24.37, \"fee\": 300, \"loan_id\": 427525, \"loan_rate\": 21.85, \"loan_amount\": 6000, \"referral_code\": \"F66FE38E-CA67-4908-9DAA-B7D7D9186615\", \"est_monthly_payment\": 165.2, \"loan_term_in_months\": 60}, {\"apr\": 23.78, \"fee\": 1750, \"loan_id\": 427527, \"loan_rate\": 19.99, \"loan_amount\": 35000, \"referral_code\": \"F66FE38E-CA67-4908-9DAA-B7D7D9186615\", \"est_monthly_payment\": 1300.55, \"loan_term_in_months\": 36}, {\"apr\": 22.35, \"fee\": 1000, \"loan_id\": 427532, \"loan_rate\": 18.59, \"loan_amount\": 20000, \"referral_code\": \"F66FE38E-CA67-4908-9DAA-B7D7D9186615\", \"est_monthly_payment\": 728.98, \"loan_term_in_months\": 36}, {\"apr\": 21.18, \"fee\": 750, \"loan_id\": 427530, \"loan_rate\": 17.45, \"loan_amount\": 15000, \"referral_code\": \"F66FE38E-CA67-4908-9DAA-B7D7D9186615\", \"est_monthly_payment\": 538.16, \"loan_term_in_months\": 36}, {\"apr\": 17.89, \"fee\": 500, \"loan_id\": 427528, \"loan_rate\": 14.23, \"loan_amount\": 10000, \"referral_code\": \"F66FE38E-CA67-4908-9DAA-B7D7D9186615\", \"est_monthly_payment\": 342.89, \"loan_term_in_months\": 36}]' WHERE user_id = %s" % userId
    cur.execute( q0 )
    myConnection.commit()

    q1 = "UPDATE user_targeting SET show_personal_loan = TRUE, show_student_loan = FALSE, user_apr = 15.79, loan_apr = 12.64, loan_savings = 154.00, loan_message = 'Save up to $100 with a personal loan', estimated_monthly_payment = 281.00 WHERE user_id = %s" % userId
    cur.execute( q1 )
    myConnection.commit()

    # make sure <user_permanent_tile> table has loans tile for the user

    q2 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 28" % userId
    cur.execute( q2 )
    result2 = str(cur.fetchone()[0])
    print "does user have record in <user_permanent_tile> table? " + result2

    if (int(result2) == 0):

        q3 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (28, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q3 )
        myConnection.commit()
        print "inserted into <user_permanent_tile> table"
    else:
        q4 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL WHERE user_id = %s AND permanent_tile_id = 28" % userId
        cur.execute( q4 )
        myConnection.commit()
        print "updated <user_permanent_tile> table"

    myConnection.close()

    print "Loans tile (w/ specific message) is available for user %s" % userId


#
# this function will make credit card offers tile (single view) visible to user, which will turn off loans tile if user has it
#

def enable_ccoffer_single(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "UPDATE user_targeting SET show_personal_loan = FALSE, show_student_loan = FALSE WHERE user_id = %s" % userId
    cur.execute( q0 )
    myConnection.commit()

    q1 = "SELECT COUNT(*) FROM user_credit_card_recommendations WHERE user_id = %s" % userId
    cur.execute( q1 )
    result1 = str(cur.fetchone()[0])

    if (int (result1) == 0):

        q2 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, display_text, created_at, updated_at, credit_worthiness, sort_order) VALUES (%s, 213, 'build_credit', 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 'poor', 2)" % userId
        q3 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, display_text, created_at, updated_at, credit_worthiness, sort_order) VALUES (%s, 224, 'build_credit', 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 'poor', 3)" % userId
        q4 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, display_text, created_at, updated_at, credit_worthiness, sort_order) VALUES (%s, 155, 'build_credit', 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 'poor', 1)" % userId
        cur.execute( q2 )
        myConnection.commit()
        cur.execute( q3 )
        myConnection.commit()
        cur.execute( q4 )
        myConnection.commit()
    
    else:

        q5 = "DELETE FROM user_credit_card_recommendations WHERE credit_worthiness IS NULL AND user_id = %s" % userId
        cur.execute( q5 )
        myConnection.commit()

        q6 = "SELECT COUNT(*) FROM user_credit_card_recommendations WHERE user_id = %s" % userId
        cur.execute( q6 )
        result6 = str(cur.fetchone()[0])

        if (int(result6) == 0):

            q7 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, display_text, created_at, updated_at, credit_worthiness, sort_order) VALUES (%s, 213, 'build_credit', 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 'poor', 2)" % userId
            q8 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, display_text, created_at, updated_at, credit_worthiness, sort_order) VALUES (%s, 7, 'build_credit', 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 'poor', 3)" % userId
            q9 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, display_text, created_at, updated_at, credit_worthiness, sort_order) VALUES (%s, 155, 'build_credit', 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 'poor', 1)" % userId
            cur.execute( q7 )
            myConnection.commit()
            cur.execute( q8 )
            myConnection.commit()
            cur.execute( q9 )
            myConnection.commit()
        
        else:

            q10 = "UPDATE user_credit_card_recommendations SET dismissed_at = NULL WHERE user_id = %s" % userId
            cur.execute( q10 )
            myConnection.commit()

    # make sure <user_permanent_tile> table has cco tile for the user

    q11 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 124" % userId
    cur.execute( q11 )
    result11 = str(cur.fetchone()[0])
    print "does user have record in <user_permanent_tile> table? " + result11

    if (int(result11) == 0):

        q12 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (124, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q12 )
        myConnection.commit()
        print "inserted into <user_permanent_tile> table"
    else:
        q13 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL WHERE user_id = %s AND permanent_tile_id = 124" % userId
        cur.execute( q13 )
        myConnection.commit()
        print "updated <user_permanent_tile> table"

    myConnection.close()

    print "CC offers tile (single card) is available for user %s" % userId


#
# this function will make credit card offers tile (multi view) visible to user, which will turn off loans tile if user has it
#

def enable_ccoffer_multi (userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "UPDATE user_targeting SET show_personal_loan = FALSE, show_student_loan = FALSE WHERE user_id = %s" % userId
    cur.execute( q0 )
    myConnection.commit()

    q1 = "SELECT COUNT(*) FROM user_credit_card_recommendations WHERE user_id = %s" % userId
    cur.execute( q1 )
    result1 = str(cur.fetchone()[0])

    if (int (result1) == 0):

        q2_0 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 116, 'cashback', 1348, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
        q2_1 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 116, 'no_annual_fee', 1348, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
        q2_2 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 116, 'low_interest', 1348, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
        q2_3 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 156, 'cashback', 2579, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
        q2_4 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 156, 'no_annual_fee', 2579, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 3)" % userId
        q2_5 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 156, 'low_interest', 2579, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
        q2_6 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 118, 'travel', 1175, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
        q2_7 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 118, 'rewards', 1175, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
        q2_8 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 18, 'no_annual_fee', 0, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
        q2_9 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 18, 'low_interest', 0, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 3)" % userId
        q2_10 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 213, 'build_credit', NULL, 2, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
        q2_11 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 11, 'travel', 421, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
        q2_12 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 11, 'rewards', 421, NULL, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
        q2_13 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, fixed, display_text, created_at, updated_at, sort_order) VALUES (%s, 155, 'build_credit', NULL, 1, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
        
        cur.execute( q2_0 )
        myConnection.commit()
        cur.execute( q2_1 )
        myConnection.commit()
        cur.execute( q2_2 )
        myConnection.commit()
        cur.execute( q2_3 )
        myConnection.commit()
        cur.execute( q2_4 )
        myConnection.commit()
        cur.execute( q2_5 )
        myConnection.commit()
        cur.execute( q2_6 )
        myConnection.commit()
        cur.execute( q2_7 )
        myConnection.commit()
        cur.execute( q2_8 )
        myConnection.commit()
        cur.execute( q2_9 )
        myConnection.commit()
        cur.execute( q2_10 )
        myConnection.commit()
        cur.execute( q2_11 )
        myConnection.commit()
        cur.execute( q2_12 )
        myConnection.commit()
        cur.execute( q2_13 )
        myConnection.commit()

    else:

        q5 = "DELETE FROM user_credit_card_recommendations WHERE credit_worthiness IS NOT NULL AND user_id = %s" % userId
        cur.execute( q5 )
        myConnection.commit()

        q6 = "SELECT COUNT(*) FROM user_credit_card_recommendations WHERE user_id = %s" % userId
        cur.execute( q6 )
        result6 = str(cur.fetchone()[0])

        if (int(result6) == 0):

            q7 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, display_text, created_at, updated_at, sort_order) VALUES (%s, 213, 'build_credit', 0, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 2)" % userId
            q8 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, display_text, created_at, updated_at, sort_order) VALUES (%s, 7, 'build_credit', 0, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 3)" % userId
            q9 = "INSERT INTO user_credit_card_recommendations (user_id, credit_card_detail_id, tag, estimated_savings, display_text, created_at, updated_at, sort_order) VALUES (%s, 155, 'build_credit', 0, 'Based on your financial activity, we have a credit card recommendation for you. Check it out.', NOW(), NOW(), 1)" % userId
            cur.execute( q7 )
            myConnection.commit()
            cur.execute( q8 )
            myConnection.commit()
            cur.execute( q9 )
            myConnection.commit()

        else:

            q10 = "UPDATE user_credit_card_recommendations SET dismissed_at = NULL WHERE user_id = %s" % userId
            cur.execute( q10 )
            myConnection.commit()

    # make sure <user_permanent_tile> table has cco tile for the user

    q11 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 124" % userId
    cur.execute( q11 )
    result11 = str(cur.fetchone()[0])
    print "does user have record in <user_permanent_tile> table? " + result11

    if (int(result11) == 0):

        q12 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (124, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q12 )
        myConnection.commit()
        print "inserted into <user_permanent_tile> table"
    else:
        q13 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL WHERE user_id = %s AND permanent_tile_id = 124" % userId
        cur.execute( q13 )
        myConnection.commit()
        print "updated <user_permanent_tile> table"

    myConnection.close()

    print "CC offers tile (multi card) is available for user %s" % userId


#
# this function will make cancel subscription tile visible to user with subscriptions that are cancellable
#

def enable_bill_cancellation(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_monthly_expense WHERE user_id = %s AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "SELECT id FROM account WHERE user_id = %s AND type = 'credit' AND deleted_at IS NULL" % userId
        cur.execute( q1 )
        user_account_number = str(cur.fetchone()[0])

        q2 = "INSERT INTO user_monthly_expense (user_id, name, amount, is_estimated, date_of_month_due, created_at, updated_at, bill_provider_id, confidence_level, is_set_by_user, period_in_days, account_number) VALUES (%s, 'Netflix', 38.00, TRUE, 3, NOW(), NOW(), 38, 1, FALSE, 32, %s)" % (userId, user_account_number)
        q2_1 = "SELECT max(id) FROM user_monthly_expense WHERE user_id = %s AND deleted_at IS NULL" % userId
        q3 = "INSERT INTO user_monthly_expense (user_id, name, amount, is_estimated, date_of_month_due, created_at, updated_at, bill_provider_id, confidence_level, is_set_by_user, account_number) VALUES (%s, 'YMCA', 868.00, TRUE, 8, NOW(), NOW(), 868, 1, FALSE, %s)" % (userId, user_account_number)
        q3_1 = "SELECT max(id) FROM user_monthly_expense WHERE user_id = %s AND deleted_at IS NULL" % userId

        cur.execute( q2 )
        myConnection.commit()
        cur.execute( q2_1 )
        maxId_1 = str(cur.fetchone()[0])

        cur.execute( q3 )
        myConnection.commit()
        cur.execute( q3_1 )
        maxId_2 = str(cur.fetchone()[0])

        q4 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, user_monthly_expense_id, is_outlier, clarity_category, pending, transaction_brand_id, plaid_date ) VALUES ('plaid', 38.00, NOW(), 'Netflix', '{Service,Subscription}', 'digital', NOW(), NOW(), %s, %s, FALSE, 'entertainment', FALSE, 38, NOW())" % (user_account_number, maxId_1)
        q5 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, user_monthly_expense_id, is_outlier, clarity_category, pending, transaction_brand_id, plaid_date ) VALUES ('plaid', 868.00, NOW(), 'YMCA', '{Recreation,\"Gyms and Fitness Centers\"}', 'place', NOW(), NOW(), %s, %s, FALSE, 'health', FALSE, 950, NOW())" % (user_account_number, maxId_2)

        cur.execute( q4 )
        myConnection.commit()
        cur.execute( q5 )
        myConnection.commit()

    else:
        q6 = "UPDATE user_monthly_expense SET user_application_id = NULL, deleted_at = NULL, dismissed_at = NULL WHERE user_id = %s AND bill_provider_id IS NOT NULL" % userId
        cur.execute( q6 )
        myConnection.commit()

        q7 = "UPDATE user_application SET deleted_at = NOW() WHERE user_id = %s AND bill_provider_id IS NOT NULL AND application_type = 'bill_cancel'" % userId
        cur.execute( q7 )
        myConnection.commit()

    q8 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 7" % userId
    cur.execute( q8 )
    result8 = str(cur.fetchone()[0])

    if (int(result8) == 0):
        q9 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (7, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q9 )
        myConnection.commit()
    else:
        q10 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL WHERE user_id = %s AND permanent_tile_id = 7" % userId
        cur.execute( q10 )
        myConnection.commit()


    # make sure <user_permanent_tile> table has bill cancelation tile for the user

    q11 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 7" % userId
    cur.execute( q11 )
    result11 = str(cur.fetchone()[0])
    print "does user have record in <user_permanent_tile> table? " + result11

    if (int(result11) == 0):

        q12 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (7, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q12 )
        myConnection.commit()
        print "inserted into <user_permanent_tile> table"
    else:
        q13 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL WHERE user_id = %s AND permanent_tile_id = 7" % userId
        cur.execute( q13 )
        myConnection.commit()
        print "updated <user_permanent_tile> table"


    myConnection.close()

    print "Cancel subscription tile is available for user %s" % userId


#
# this function will complete bill cancellation application which will allow the user to make payments
#

def cancellation_complete_application(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "UPDATE user_application SET status = 'success', charge_amount = 1.00, requires_payment = TRUE WHERE user_id = %s AND application_type = 'bill_cancel' AND status = 'pending' AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    myConnection.commit()

    myConnection.close()

    print "Cancel subscription tile (complete application) is available for user %s" % userId

#
# this function will make bill negotiation tile visible to user with bills that are negotiable
#

def enable_bill_negotiation (userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_monthly_expense WHERE user_id = %s AND bill_provider_id IN(34,7)" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    q1 = "SELECT account_number FROM account WHERE user_id = %s AND type = 'credit' AND deleted_at IS NULL" % userId
    cur.execute( q1 )
    user_account_number = str(cur.fetchone()[0])
    
    if (int(result0) == 0):

        q2 = "SELECT account_number FROM account WHERE user_id = %s AND type = 'credit' AND deleted_at IS NULL" % userId
        cur.execute( q2 )
        user_account_number = str(cur.fetchone()[0])

        q3 = "SELECT id FROM account WHERE user_id = %s AND account_number = %s AND deleted_at IS NULL" % (userId, user_account_number)
        cur.execute( q3 )
        user_account_id = str(cur.fetchone()[0])

        q4 = "INSERT INTO user_monthly_expense (user_id, name, amount, is_estimated, date_of_month_due, created_at, updated_at, bill_provider_id, confidence_level, is_set_by_user, period_in_days, account_number) VALUES (%s, 'Verizon Wireless', 134.00, TRUE, 3, NOW(), NOW(), 34, 1, FALSE, 32, %s)" % (userId, user_account_number)
        q5 = "INSERT INTO user_monthly_expense (user_id, name, amount, is_estimated, date_of_month_due, created_at, updated_at, bill_provider_id, confidence_level, is_set_by_user, account_number) VALUES (%s, 'Time Warner Cable', 107.00, TRUE, 8, NOW(), NOW(), 7, 1, FALSE, %s)" % (userId, user_account_number)
        cur.execute( q4 )
        myConnection.commit()
        cur.execute( q5 )
        myConnection.commit()

        q6 = "SELECT id FROM user_monthly_expense WHERE user_id = %s AND name = 'Verizon Wireless' " % userId
        user_monthly_expense_vw = cur.execute( q6 )
        
        q7 = "SELECT id FROM user_monthly_expense WHERE user_id = %s AND name = 'Time Warner Cable' " % userId
        user_monthly_expense_twc = cur.execute( q7 )

        q8 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, user_monthly_expense_id, is_outlier, clarity_category, pending, transaction_brand_id, plaid_date) VALUES ('plaid', 134.00, NOW(), 'Verizon Wireless', '{Service, \"Telecommunication Services\"}', 'place', NOW(), NOW(), %s, %s, FALSE, 'bills', FALSE, 911, NOW() )" % (user_account_id, user_monthly_expense_vw)
        q9 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, user_monthly_expense_id, is_outlier, clarity_category, pending, transaction_brand_id, plaid_date) VALUES ('plaid', 107.00, NOW(), 'Time Warner Cable', '{Service, Cable}, 'special', NOW(), NOW(), %s, %s, FALSE, 'bills', FALSE, 864, NOW() )" % (user_account_id, user_monthly_expense_twc)
        
        cur.execute( q8 )
        myConnection.commit()
        cur.execute( q9 )
        myConnection.commit()

    else:
        q10 = "UPDATE user_monthly_expense SET user_application_id = NULL, deleted_at = NULL, dismissed_at = NULL WHERE user_id = %s AND bill_provider_id IS NOT NULL" % userId
        cur.execute( q10 )
        myConnection.commit()

        q11 = "UPDATE user_application SET deleted_at = NOW() WHERE user_id = %s AND bill_provider_id IS NOT NULL AND application_type = 'bill_negotiate'" % userId
        cur.execute( q11 )
        myConnection.commit()

        q12 = "SELECT account_number FROM account WHERE user_id = %s AND type = 'credit' AND deleted_at IS NULL" % userId
        cur.execute( q12 )
        user_account_number = str(cur.fetchone()[0])

        q13 = "SELECT id FROM account WHERE user_id = %s AND account_number = %s AND deleted_at IS NULL" % (userId, user_account_number)
        cur.execute( q13 )
        user_account_id = str(cur.fetchone()[0])


        q14 = "SELECT id FROM user_monthly_expense WHERE user_id = %s AND name = 'Verizon Wireless' " % userId
        user_monthly_expense_vw = cur.execute( q14 )
        
        q15 = "SELECT id FROM user_monthly_expense WHERE user_id = %s AND name = 'Time Warner Cable' " % userId
        user_monthly_expense_twc = cur.execute( q15 )

        q16 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, user_monthly_expense_id, is_outlier, clarity_category, pending, transaction_brand_id, plaid_date) VALUES ('plaid', 134.00, NOW(), 'Verizon Wireless', '{Service, \"Telecommunication Services\"}', 'place', NOW(), NOW(), %s, %s, FALSE, 'bills', FALSE, 911, NOW() )" % (user_account_id, user_monthly_expense_vw)
        q17 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, user_monthly_expense_id, is_outlier, clarity_category, pending, transaction_brand_id, plaid_date) VALUES ('plaid', 107.00, NOW(), 'Time Warner Cable', '{Service, Cable}, 'special', NOW(), NOW(), %s, %s, FALSE, 'bills', FALSE, 864, NOW() )" % (user_account_id, user_monthly_expense_twc)
        
        cur.execute( q16 )
        myConnection.commit()
        cur.execute( q17 )
        myConnection.commit()

        q18 = "INSERT INTO transaction (source, amount, date, name, created_at, updated_at, account_id, is_outlier, pending, plaid_date) VALUES ('plaid', 34.00, NOW(), 'Verizon Wireless', NOW(), NOW(), %s, FALSE, FALSE, NOW() )" % (user_account_id)
        q19 = "INSERT INTO transaction (source, amount, date, name, created_at, updated_at, account_id, is_outlier, pending, plaid_date) VALUES ('plaid', 7.00, NOW(), 'Time Warner Cable', NOW(), NOW(), %s, FALSE, FALSE, NOW() )" % (user_account_id)
        
        cur.execute( q18 )
        myConnection.commit()
        cur.execute( q19 )
        myConnection.commit()

    q20 = "SELECT COUNT(*) FROM user_insight WHERE user_id = %s AND insight_id = 28" % userId
    cur.execute( q20 )
    result20 = str(cur.fetchone()[0])

    if (int(result20) == 0):
        q21 = "INSERT INTO user_insight (insight_id, user_id, created_at, updated_at, data, action_likelihood) VALUES (28, %s, NOW(), NOW(), '[{\"token\":\"billNames\",\"string\":\"Verizon Wireless and Time Warner Cable\",\"value\":null,\"type\":null},{\"token\":\"passCodes\",\"string\":\"\",\"value\":[{\"name\":\"Passcode for Verizon Wireless\",\"id\":\"verizon_wireless\"}],\"type\":\"object\"},{\"token\":\"bills\",\"string\":\"\",\"value\":[{\"id\":657799,\"passcodeName\":\"Passcode for Verizon Wireless\",\"passcodeId\":\"verizon_wireless\",\"name\":\"Verizon Wireless\",\"amount\":\"$1,045/yr\",\"logoUrl\":\"https://static.claritymoney.com/images/logos/brands/verizon_wireless.png\"},{\"id\":657882,\"passcodeName\":null,\"passcodeId\":null,\"name\":\"Time Warner Cable\",\"amount\":\"$1,418/yr\",\"logoUrl\":\"https://static.claritymoney.com/images/logos/brands/time_warner_cable.jpg\"}],\"type\":\"object\"}]', 1)" % userId
        cur.execute( q21 )
        myConnection.commit()
    else:
        q22 = "UPDATE user_insight SET seen_at = NULL, acted_at = NULL, deleted_at = NULL, dismissed_at = NULL WHERE user_id = %s AND insight_id = 28" % userId
        cur.execute( q22 )
        myConnection.commit()

    myConnection.close()

    print "Bill negotiation tile is available for user %s" % userId

#
# this function will complete bill negotiation application which will allow the user to make payments
#

def negotiation_complete_application(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "UPDATE user_application SET status = 'success', sub_status = 'success', wait_until = NULL, charge_amount = 1.00, requires_payment = TRUE WHERE user_id = %s AND application_type = 'bill_negotiate' AND status = 'waiting' AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    myConnection.commit()

    myConnection.close()

    print "Bill negotiation tile (complete application) is available for user %s" % userId


#
# this function will display the income insigt tile with one button where the app does not know user income
#

def enable_income_insight_one(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_insight WHERE user_id = %s" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    q1 = "SELECT COUNT(*) FROM user_income WHERE user_id = %s" % userId
    cur.execute( q1 )
    result1 = str(cur.fetchone()[0])

    if (int(result0) == 0 and int(result1) == 0):

        q2 = "INSERT INTO user_insight (insight_id, user_id, created_at, updated_at, data, action_likelihood) VALUES (1, %s, NOW(), NOW(), '[{\"token\":\"incomeTitle\",\"string\":\"We need your Income\",\"value\":null,\"type\":null},{\"token\":\"estimateString\",\"string\":\"We will get to work as soon we have this\",\"value\":null,\"type\":null}]', 1)" % userId
        cur.execute( q2 )
        myConnection.commit()

        q3 = "INSERT INTO user_income (monthly_income, created_at, updated_at, user_id, is_estimated, user_monthly_income) VALUES (1000, NOW(), NOW(), %s, FALSE, 0)" % userId
        cur.execute( q3 )
        myConnection.commit()

    else:

        q4 = "UPDATE user_insight SET seen_at = NULL, acted_at = NULL, deleted_at = NULL, dismissed_at = NULL, data = '[{\"token\":\"incomeTitle\",\"string\":\"We need your Income\",\"value\":null,\"type\":null},{\"token\":\"estimateString\",\"string\":\"We will get to work as soon we have this\",\"value\":null,\"type\":null}]', action_likelihood = 1 WHERE user_id = %s AND insight_id = 1" % userId
        cur.execute( q4 )
        myConnection.commit()

        q5 = "SELECT max(id) FROM user_income WHERE user_id = %s" % userId
        cur.execute( q5 )
        userIncomeId = str(cur.fetchone()[0])

        q6 = "UPDATE user_income SET user_monthly_income = 0, deleted_at = NULL, is_estimated = FALSE WHERE user_id = %s AND id = %s" % (userId, userIncomeId)
        cur.execute( q6 )
        myConnection.commit()

    myConnection.close()

    print "Income insight tile (w/ one button) is available for user %s" % userId


#
# this function will display income insight tile with two buttons where app has an estimate of user income based on income transactions
#

def enable_income_insight_two(userId):
    
    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_insight WHERE user_id = %s" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    q1 = "SELECT COUNT(*) FROM user_income WHERE user_id = %s" % userId
    cur.execute( q1 )
    result1 = str(cur.fetchone()[0])
    print result1

    if (int(result0) == 0 and int(result1) == 0):

        q2 = "INSERT INTO user_insight (insight_id, user_id, created_at, updated_at, data, action_likelihood) VALUES (1, %s, NOW(), NOW(), '[{\"token\":\"incomeTitle\",\"string\":\"How Did We Do?\",\"value\":null,\"type\":null},{\"token\":\"estimateString\",\"string\":\"We estimated your Monthly Income as $1234.\",\"value\":null,\"type\":null},{\"token\":\"promptValue\",\"string\":\"\",\"value\":{\"id\":2690,\"monthly_income\":1234,\"is_estimated\":true,\"income_frequency\":null,\"user_id\":%s},\"type\":\"currency\"}]', 1)" % (userId, userId)
        cur.execute( q2 )
        myConnection.commit()

        q3 = "INSERT INTO user_income (monthly_income, created_at, updated_at, user_id, is_estimated, user_monthly_income) VALUES (1000, NOW(), NOW(), %s, TRUE, 1234)" % userId
        cur.execute( q3 )
        myConnection.commit()

    elif(int(result0) != 0 and int(result1) == 0):

        q3_1 = "INSERT INTO user_income (monthly_income, created_at, updated_at, user_id, is_estimated, user_monthly_income) VALUES (1000, NOW(), NOW(), %s, TRUE, 1234)" % userId
        cur.execute( q3_1 )
        myConnection.commit()

    else:

        q4 = "UPDATE user_insight SET seen_at = NULL, acted_at = NULL, deleted_at = NULL, dismissed_at = NULL, data = '[{\"token\":\"incomeTitle\",\"string\":\"How Did We Do?\",\"value\":null,\"type\":null},{\"token\":\"estimateString\",\"string\":\"We estimated your Monthly Income as $1234\",\"value\":null,\"type\":null},{\"token\":\"promptValue\",\"string\":\"\",\"value\":{\"id\":2690,\"monthly_income\":1234,\"is_estimated\":true,\"income_frequency\":null,\"user_id\":%s},\"type\":\"currency\"}]', action_likelihood = 1 WHERE user_id = %s AND insight_id = 1" % (userId, userId)
        cur.execute( q4 )
        myConnection.commit()

        q5 = "SELECT max(id) FROM user_income WHERE user_id = %s" % userId
        cur.execute( q5 )
        userIncomeId = str(cur.fetchone()[0])

        q6 = "UPDATE user_income SET user_monthly_income = 1234, deleted_at = NULL WHERE user_id = %s AND id = %s" % (userId, userIncomeId)
        cur.execute( q6 )
        myConnection.commit()

    myConnection.close()

    print "Income insight tile (w/ two button) is available for user %s" % userId


#
# this function will display acorns tile
#

def enable_acorns_signup(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 123" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (123, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 123" % userId
        cur.execute( q2 )
        myConnection.commit()

    q3 = "SELECT COUNT(*) FROM user_targeting WHERE user_id = %s" % userId
    cur.execute( q3 )
    result3 = str(cur.fetchone()[0])

    if (int(result3) != 0):

        q4 = "UPDATE user_targeting SET show_acorns = FALSE WHERE user_id = %s" % userId
        cur.execute( q4 )
        myConnection.commit()
    
    else:
        q5 = "INSERT INTO user_targeting (user_id, show_acorns, show_personal_loan, created_at, updated_at, is_account_verifiable, show_student_loan) VALUES (%s, FALSE, FALSE, NOW(), NOW(), TRUE, FALSE)" % userId
        cur.execute( q5 )
        myConnection.commit()

    myConnection.close()

    print "Acorns tile (w/ signup) is available for user %s" % userId


#
# this function will display acorns tile
#

def enable_acorns_signin(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 123" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (123, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 123" % userId
        cur.execute( q2 )
        myConnection.commit()

    q3 = "SELECT COUNT(*) FROM user_targeting WHERE user_id = %s" % userId
    cur.execute( q3 )
    result3 = str(cur.fetchone()[0])

    if (int(result3) != 0):

        q4 = "UPDATE user_targeting SET show_acorns = TRUE WHERE user_id = %s" % userId
        cur.execute( q4 )
        myConnection.commit()


    myConnection.close()

    print "Acorns tile (w/ signin) is available for user %s" % userId


#
# this function will display notifications tile
#

def enable_notifications(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 18" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (18, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 18" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "Notifications tile is available for user %s" % userId


#
# this function will display refer friend tile
#

def enable_referFriend(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 22" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (22, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 22" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "Refer friend tile is available for user %s" % userId


#
# this function will display siri tile (only on iOS 11.x or higher)
#

def enable_siri(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 129" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (129, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 129" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "Siri tile is available for user %s" % userId



#
# this function will display connect more accounts tile
#

def enable_moreAccounts(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 24" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (24, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 24" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "Connect more accounts tile is available for user %s" % userId



#
# this function will display credit utilization tile
#

def enable_creditUtilization(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 2" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (2, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 2" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "Credit utilization tile is available for user %s" % userId



#
# this function will display how it works tile
#

def enable_howItWorks(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 23" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (23, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 23" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "How it works tile is available for user %s" % userId


#
# this function will display income this month tile
#

def enable_incomeThisMonth(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT id FROM account WHERE user_id = %s AND type = 'depository' AND sub_type = 'checking' " % userId
    cur.execute( q0 )
    user_account_id = str(cur.fetchone()[0])

    q2 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', -21.00, NOW(), 'Income', '{Transfer, Payroll}', 'special', NOW(), NOW(), %s, FALSE, 'regular income', FALSE, NOW() )" % (user_account_id)
    cur.execute( q2 )
    myConnection.commit()

    q3 = "SELECT COUNT(*) FROM user_income WHERE user_id = %s " % userId
    cur.execute( q3 )
    result3 = str(cur.fetchone()[0])

    if (int(result3) == 0 or result3 is None):
        q4 = "INSERT INTO user_income (monthly_income, created_at, updated_at, user_id, is_estimated, effective_date) VALUES (1234, NOW(), NOW(), %s, TRUE, NOW()) " % userId
        cur.execute( q4 )

    else:
        q5 = "SELECT max(id) FROM user_income WHERE user_id = %s " % userId
        cur.execute( q5 )
        maxId = str(cur.fetchone()[0])

        q6 = "UPDATE user_income SET monthly_income = 100, created_at = NOW(), updated_at = NOW(), deleted_at = NOW(), is_estimated = TRUE WHERE user_id = %s AND id = %s " % (userId, maxId)
        cur.execute( q6 )

    myConnection.close()

    print "Income This Month tile is available for user %s" % userId


#
# this function will display next paycheck tile
#

def enable_nextPaycheck(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    n0 = 90
    n1 = 60
    n2 = 30

    date_90_days_ago = (datetime.now() - timedelta(days=n0)).strftime('%Y-%m-%d')
    date_90 = (datetime.now() - timedelta(days=n0))
    date_60_days_ago = (datetime.now() - timedelta(days=n1)).strftime('%Y-%m-%d')
    date_60 = (datetime.now() - timedelta(days=n1))
    date_30_days_ago = (datetime.now() - timedelta(days=n2)).strftime('%Y-%m-%d')
    date_30 = (datetime.now() - timedelta(days=n2))

    q0 = "SELECT id FROM account WHERE user_id = %s AND type = 'depository' AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    user_account_id = str(cur.fetchone()[0])
    
    q1 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', -555.00, \'%s\', 'Income', '{Transfer, Payroll}', 'special',  \'%s\', \'%s\', %s, FALSE, 'regular income', FALSE, \'%s\' )" % (date_90_days_ago, date_90, date_90, user_account_id, date_90_days_ago)
    cur.execute( q1 )
    myConnection.commit()

    q2 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', -555.00, \'%s\', 'Income', '{Transfer, Payroll}', 'special',  \'%s\', \'%s\', %s, FALSE, 'regular income', FALSE, \'%s\' )" % (date_60_days_ago, date_60, date_60, user_account_id, date_60_days_ago)
    cur.execute( q2 )
    myConnection.commit()

    q3 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', -555.00, \'%s\', 'Income', '{Transfer, Payroll}', 'special', \'%s\', \'%s\', %s, FALSE, 'regular income', FALSE, \'%s\' )" % (date_30_days_ago, date_30, date_30, user_account_id, date_30_days_ago)
    cur.execute( q3 )
    myConnection.commit()

    q4 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', -555.00, NOW(), 'Income', '{Transfer, Payroll}', 'special', NOW(), NOW(), %s, FALSE, 'regular income', FALSE, NOW() )" % (user_account_id)
    cur.execute( q4 )
    myConnection.commit()

    q5 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 26" % userId
    cur.execute( q5 )
    myConnection.commit()

    q6 = "INSERT INTO user_income_analysis (next_paycheck_date, most_recent_paycheck_transaction_id, created_at, updated_at, user_id) values (NOW(), 6330403, NOW(), NOW(), %s)" % userId
    cur.execute( q6 )
    myConnection.commit()

    myConnection.close()

    print "Next paycheck tile is available for user %s" % userId


def enable_creditCardDue (userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    n0 = 2
    due_date = (datetime.now() + timedelta(days=n0)).strftime('%Y-%m-%d')

    q0 = "SELECT id FROM account WHERE user_id = %s AND type = 'credit' AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    user_account_id = str(cur.fetchone()[0])

    q1 = "UPDATE account_balance SET current_balance = 555 WHERE account_id = %s" % user_account_id
    cur.execute( q1 )
    myConnection.commit()

    q2 = "UPDATE account_meta SET next_bill_due_date = \'%s\' WHERE account_id = %s" % (due_date, user_account_id)
    cur.execute( q2 )
    myConnection.commit()

    q3 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 25" % userId
    cur.execute( q3 )
    myConnection.commit()

    myConnection.close()

    print "Credit card due tile is available for user %s" % userId

#
# this function will display thank you tile
#

def enable_thankYou(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT COUNT(*) FROM user_permanent_tile WHERE user_id = %s AND permanent_tile_id = 14" % userId
    cur.execute( q0 )
    result0 = str(cur.fetchone()[0])

    if (int(result0) == 0):

        q1 = "INSERT INTO user_permanent_tile (permanent_tile_id, user_id, created_at, updated_at, action_likelihood) VALUES (14, %s, NOW(), NOW(), 1)" % userId
        cur.execute( q1 )
        myConnection.commit()
    
    else:

        q2 = "UPDATE user_permanent_tile SET deleted_at = NULL, dismissed_at = NULL, acted_at = NULL, action_likelihood = 1 WHERE user_id = %s AND permanent_tile_id = 14" % userId
        cur.execute( q2 )
        myConnection.commit()

    myConnection.close()

    print "Thank you tile is available for user %s" % userId


def load_transactions (userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "SELECT id FROM account WHERE user_id = %s AND type = 'credit' AND deleted_at IS NULL" % userId
    cur.execute( q0 )
    user_account_id = str(cur.fetchone()[0])
    print user_account_id

    q1 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1001.00, NOW(), 'Transaction Food A', '{\"Food and Drink\",Restaurants}', 'place', NOW(), NOW(), %s, FALSE, 'food', FALSE, NOW() )" % (user_account_id)
    q2 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1002.00, NOW(), 'Transaction Shopping A', '{Shops,\"Supermarkets and Groceries\"}', 'place', NOW(), NOW(), %s, FALSE, 'shopping', FALSE, NOW() )" % (user_account_id)
    q3 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1003.00, NOW(), 'Transaction Health A', '{Healthcare,\"Healthcare Services\"}', 'place', NOW(), NOW(), %s, FALSE, 'service', FALSE, NOW() )" % (user_account_id)
    q4 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1004.00, NOW(), 'Transaction Services A','{Community,\"Government Departments and Agencies\"}', 'place', NOW(), NOW(), %s, FALSE, 'service', FALSE, NOW() )" % (user_account_id)
    q5 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1005.00, NOW(), 'Transaction Travel A','{Travel,\"Public Transportation Services\"}' , 'place', NOW(), NOW(), %s, FALSE, 'travel', FALSE, NOW() )" % (user_account_id)
    q6 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1006.00, NOW(), 'Transaction Services B', '{Service,Subscription}', 'place', NOW(), NOW(), %s, FALSE, 'service', FALSE, NOW() )" % (user_account_id)
    q7 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1007.00, NOW(), 'Transaction Health B', '{Healthcare,\"Healthcare Services\"}', 'place', NOW(), NOW(), %s, FALSE, 'health', FALSE, NOW() )" % (user_account_id)
    q8 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1008.00, NOW(), 'Transaction Food B','{\"Food and Drink\",Restaurants}', 'place', NOW(), NOW(), %s, FALSE, 'food', FALSE, NOW() )" % (user_account_id)
    q9 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1009.00, NOW(), 'Transaction Shopping B','{Shops,\"Supermarkets and Groceries\"}', 'place', NOW(), NOW(), %s, FALSE, 'shopping', FALSE, NOW() )" % (user_account_id)
    q10 = "INSERT INTO transaction (source, amount, date, name, category, type, created_at, updated_at, account_id, is_outlier, clarity_category, pending, plaid_date) VALUES ('plaid', 1010.00, NOW(), 'Transaction Travel B', '{Travel,\"Public Transportation Services\"}', 'place', NOW(), NOW(), %s, FALSE, 'travel', FALSE, NOW() )" % (user_account_id)

    cur.execute( q1 )
    myConnection.commit()
    cur.execute( q2 )
    myConnection.commit()
    cur.execute( q3 )
    myConnection.commit()
    cur.execute( q4 )
    myConnection.commit()
    cur.execute( q5 )
    myConnection.commit()
    cur.execute( q6 )
    myConnection.commit()
    cur.execute( q7 )
    myConnection.commit()
    cur.execute( q8 )
    myConnection.commit()
    cur.execute( q9 )
    myConnection.commit()
    cur.execute( q10 )
    myConnection.commit()

    myConnection.close()

    print "Transactions are available for user %s" % userId

def reset_interstitials(userId):

    myConnection = pgdb.connect( host=hostname, user=username, password=password, database=database )
    cur = myConnection.cursor()

    q0 = "UPDATE user SET email_verified = NULL WHERE user_id = %s" % userId
    cur.execute( q0 )
    myConnection.commit()
    
    q1 = "UPDATE user SET is_mfa_required = TRUE WHERE user_id = %s" % userId
    cur.execute( q1 )
    myConnection.commit()

    q2 = "UPDATE user SET terms_accepted_at = NULL WHERE user_id = %s" % userId
    cur.execute( q2 )
    myConnection.commit()

    q3 = "UPDATE user SET password_secured_at = NULL WHERE user_id = %s" % userId
    cur.execute( q3 )
    myConnection.commit()
    
    myConnection.close()

    print "User %s is reset" % userId



if __name__ == '__main__':
    
    #enable_bill_cancellation('1746')
    #cancellation_complete_application('1912')
    #enable_creditUtilization('2406')
    #enable_income_insight_one('1838')
    #enable_ccoffer_single('2406')

    '''
    enable_creditUtilization('1407')
    enable_siri('1407')
    enable_referFriend('1407')
    '''
    #enable_lemonade('1424')
    #enable_sofi('1424')
    '''
    enable_notifications('1407')
    enable_howItWorks('1407')
    enable_thankYou('1407')
    '''

    #enable_income_insight_one('1424')

    #enable_ccoffer_single('1407')

    #enable_income_insight_two('1746')
    #############################
    # new users

    #reset_savings_tile('1681')
    #savings_noKyc_failTerms('1681')


    #reset_savings_tile('1746')
    #bonus_with_savings_paused('1746')
    #savings_passKyc_failTerms('1746')

##################################
    # active users

    #reset_savings_tile('1794')
    #bonus_with_savings('1794')  
    #savings_noKyc_failTerms('1794')


    #reset_savings_tile('1838')
    #bonus_with_savings('1838')
    #savings_passKyc_failTerms('1838')

###################################
    # paused users

    #reset_savings_tile('1848')
    #bonus_with_savings_paused('1848')
    #savings_noKyc_failTerms('1848')


    #reset_savings_tile('1860')
    #bonus_with_savings_paused('1860')
    #savings_passKyc_failTerms('1860')

    ##################################
    # referral bonus

    #reset_savings_tile('1959')
    #bonus_without_savings('1959')
    #savings_noKyc_failTerms('1959')


    #reset_savings_tile('1964')
    #bonus_without_savings('1964')
    #savings_passKyc_failTerms('1964')

    ###################################
    #failed users

    #reset_savings_tile('1949')
    #bonus_with_savings('1949')
    #savings_failKyc_passTerms('1949')

    #reset_savings_tile('1954')
    #bonus_with_savings_paused('1954')
    #savings_failKyc_passTerms('1954')


    #######################################   
    #######################################
    #
    # new users who need full kyc
    #

    '''
    reset_savings_tile('1679')
    reset_savings_tile('1680')
    reset_savings_tile('1682')
    reset_savings_tile('1683')
    reset_savings_tile('1690')
    reset_savings_tile('1718')
    reset_savings_tile('1731')
    '''

    '''
    savings_noKyc_failTerms('1679')
    savings_noKyc_failTerms('1680')
    savings_noKyc_failTerms('1682')
    savings_noKyc_failTerms('1683')
    savings_noKyc_failTerms('1690')
    savings_noKyc_failTerms('1718')
    savings_noKyc_failTerms('1731')
    '''

    ##################################
    #
    # new users who do NOT need full kyc
    #

    '''
    reset_savings_tile('1733')
    reset_savings_tile('1736')
    reset_savings_tile('1738')
    reset_savings_tile('1743')
    reset_savings_tile('1747')
    reset_savings_tile('1754')
    reset_savings_tile('1762')
    reset_savings_tile('1763')
    reset_savings_tile('1767')
    '''

    '''
    savings_passKyc_failTerms('1733')
    savings_passKyc_failTerms('1736')
    savings_passKyc_failTerms('1738')
    savings_passKyc_failTerms('1743')
    savings_passKyc_failTerms('1747')
    savings_passKyc_failTerms('1754')
    savings_passKyc_failTerms('1762')
    savings_passKyc_failTerms('1762')
    savings_passKyc_failTerms('1763')
    savings_passKyc_failTerms('1767')
    '''

    ####################################
    #
    # active users who need full kyc (no saved money)
    #

    '''
    reset_savings_tile('1965')
    reset_savings_tile('1966')
    reset_savings_tile('2032')
    reset_savings_tile('2034')
    reset_savings_tile('2036')
    '''

    '''
    create_savings('1965')
    create_savings('1966')
    create_savings('2032')
    create_savings('2034')
    create_savings('2036')
    '''

    '''
    savings_noKyc_failTerms('1965')
    savings_noKyc_failTerms('1966')
    savings_noKyc_failTerms('2032')
    savings_noKyc_failTerms('2034')
    savings_noKyc_failTerms('2036')
    '''

    ####################################
    #
    # active users who need full kyc (w/ saved money)
    #

    '''
    reset_savings_tile('1772')
    reset_savings_tile('1773')
    reset_savings_tile('1782')
    reset_savings_tile('1783')
    reset_savings_tile('1795')
    reset_savings_tile('1797')
    reset_savings_tile('1799')
    reset_savings_tile('1812')
    reset_savings_tile('1813')
    '''

    '''
    bonus_with_savings('1772')
    bonus_with_savings('1773')
    bonus_with_savings('1782')
    bonus_with_savings('1783')
    bonus_with_savings('1795')
    bonus_with_savings('1797')
    bonus_with_savings('1799')
    bonus_with_savings('1812')
    bonus_with_savings('1813')
    '''

    '''
    savings_noKyc_failTerms('1772')
    savings_noKyc_failTerms('1773')
    savings_noKyc_failTerms('1782')
    savings_noKyc_failTerms('1783')
    savings_noKyc_failTerms('1795')
    savings_noKyc_failTerms('1797')
    savings_noKyc_failTerms('1799')
    savings_noKyc_failTerms('1812')
    savings_noKyc_failTerms('1813')
    '''

    #################################
    #
    # active users who do NOT need full kyc (with saved money)
    #
    
    '''
    reset_savings_tile('1834')
    reset_savings_tile('1835')
    reset_savings_tile('1836')
    reset_savings_tile('1837')
    reset_savings_tile('1839')
    reset_savings_tile('1840')
    reset_savings_tile('1841')
    reset_savings_tile('1842')
    reset_savings_tile('1843')
    '''
    
    '''
    bonus_with_savings('1834')
    bonus_with_savings('1835')
    bonus_with_savings('1836')
    bonus_with_savings('1837')
    bonus_with_savings('1839')
    bonus_with_savings('1840')
    bonus_with_savings('1841')
    bonus_with_savings('1842')
    bonus_with_savings('1843')
    '''
    
    '''
    savings_passKyc_failTerms('1834')
    savings_passKyc_failTerms('1835')
    savings_passKyc_failTerms('1836')
    savings_passKyc_failTerms('1837')
    savings_passKyc_failTerms('1839')
    savings_passKyc_failTerms('1840')
    savings_passKyc_failTerms('1841')
    savings_passKyc_failTerms('1842')
    savings_passKyc_failTerms('1843')
    '''

    ##################################
    #
    # paused users who need full kyc
    #

    '''
    reset_savings_tile('1844')
    reset_savings_tile('1845')
    reset_savings_tile('1846')
    reset_savings_tile('1847')
    reset_savings_tile('1849')
    reset_savings_tile('1850')
    reset_savings_tile('1851')
    reset_savings_tile('1852')
    reset_savings_tile('1853')
    '''

    '''
    bonus_with_savings_paused('1844')
    bonus_with_savings_paused('1845')
    bonus_with_savings_paused('1846')
    bonus_with_savings_paused('1847')
    bonus_with_savings_paused('1849')
    bonus_with_savings_paused('1850')
    bonus_with_savings_paused('1851')
    bonus_with_savings_paused('1852')
    bonus_with_savings_paused('1853')
    '''
    
    '''
    savings_noKyc_failTerms('1844')
    savings_noKyc_failTerms('1845')
    savings_noKyc_failTerms('1846')
    savings_noKyc_failTerms('1847')
    savings_noKyc_failTerms('1849')
    savings_noKyc_failTerms('1850')
    savings_noKyc_failTerms('1851')
    savings_noKyc_failTerms('1852')
    savings_noKyc_failTerms('1853')
    '''

    ##################################
    # paused users who need full kyc  (no saved money)
    #

    '''
    reset_savings_tile('1940')
    reset_savings_tile('1941')
    reset_savings_tile('1942')
    reset_savings_tile('1943')
    reset_savings_tile('1944')
    '''

    '''
    savings_paused('1940')
    savings_paused('1941')
    savings_paused('1942')
    savings_paused('1943')
    savings_paused('1944')
    '''

    '''
    savings_noKyc_failTerms('1940')
    savings_noKyc_failTerms('1941')
    savings_noKyc_failTerms('1942')
    savings_noKyc_failTerms('1943')
    savings_noKyc_failTerms('1944')
    '''


    ##################################
    #
    # paused users who do NOT need full kyc
    #
    
    '''
    reset_savings_tile('1856')
    reset_savings_tile('1857')
    reset_savings_tile('1858')
    reset_savings_tile('1859')
    reset_savings_tile('1863')
    reset_savings_tile('1864')
    reset_savings_tile('1865')
    reset_savings_tile('1866')
    reset_savings_tile('1867')
    '''

    '''
    bonus_with_savings_paused('1856')
    bonus_with_savings_paused('1857')
    bonus_with_savings_paused('1858')
    bonus_with_savings_paused('1859')
    bonus_with_savings_paused('1863')
    bonus_with_savings_paused('1864')
    bonus_with_savings_paused('1865')
    bonus_with_savings_paused('1866')
    bonus_with_savings_paused('1867')
    '''
    
    '''
    savings_passKyc_failTerms('1856')
    savings_passKyc_failTerms('1857')
    savings_passKyc_failTerms('1858')
    savings_passKyc_failTerms('1859')
    savings_passKyc_failTerms('1863')
    savings_passKyc_failTerms('1864')
    savings_passKyc_failTerms('1865')
    savings_passKyc_failTerms('1866')
    savings_passKyc_failTerms('1867')
    '''

    ################################
    # referral bonus
    
    '''
    reset_savings_tile('1955')
    reset_savings_tile('1956')
    reset_savings_tile('1957')
    reset_savings_tile('1958')
    '''
    '''
    bonus_without_savings('1955')
    bonus_without_savings('1956')
    bonus_without_savings('1957')
    bonus_without_savings('1958')
    '''

    
    #savings_noKyc_failTerms('1955')
    #savings_noKyc_failTerms('1956')
    '''
    savings_noKyc_failTerms('1957')
    '''
    #savings_noKyc_failTerms('1958')
    
    #-----------------------------
    
    '''
    reset_savings_tile('1960')
    reset_savings_tile('1961')
    reset_savings_tile('1962')
    reset_savings_tile('1963')
    '''

    '''
    bonus_without_savings('1960')
    bonus_without_savings('1961')
    bonus_without_savings('1962')
    bonus_without_savings('1963')
    '''

    '''
    savings_passKyc_failTerms('1960')
    savings_passKyc_failTerms('1961')
    savings_passKyc_failTerms('1962')
    savings_passKyc_failTerms('1963')
    '''

    #################################
    # success state: active users

    '''
    reset_savings_tile('1920')
    reset_savings_tile('1921')
    reset_savings_tile('1922')
    reset_savings_tile('1923')
    reset_savings_tile('1924')
    reset_savings_tile('1925')
    reset_savings_tile('1926')
    reset_savings_tile('1927')
    reset_savings_tile('1928')
    reset_savings_tile('1929')
    '''

    '''
    bonus_with_savings('1920')
    bonus_with_savings('1921')
    bonus_with_savings('1922')
    bonus_with_savings('1923')
    bonus_with_savings('1924')
    bonus_with_savings('1925')
    bonus_with_savings('1926')
    bonus_with_savings('1927')
    bonus_with_savings('1928')
    bonus_with_savings('1929')
    '''

    '''
    savings_passKyc_passTerms('1920')
    savings_passKyc_passTerms('1921')
    savings_passKyc_passTerms('1922')
    savings_passKyc_passTerms('1923')
    savings_passKyc_passTerms('1924')
    savings_passKyc_passTerms('1925')
    savings_passKyc_passTerms('1926')
    savings_passKyc_passTerms('1927')
    savings_passKyc_passTerms('1928')
    savings_passKyc_passTerms('1929')
    '''

    #################################
    # success state: paused users

    '''
    reset_savings_tile('1930')
    reset_savings_tile('1931')
    reset_savings_tile('1932')
    reset_savings_tile('1933')
    reset_savings_tile('1934')
    reset_savings_tile('1935')
    reset_savings_tile('1936')
    reset_savings_tile('1937')
    reset_savings_tile('1938')
    reset_savings_tile('1939')
    '''

    '''
    bonus_with_savings_paused('1930')
    bonus_with_savings_paused('1931')
    bonus_with_savings_paused('1932')
    bonus_with_savings_paused('1933')
    bonus_with_savings_paused('1934')
    bonus_with_savings_paused('1935')
    bonus_with_savings_paused('1936')
    bonus_with_savings_paused('1937')
    bonus_with_savings_paused('1938')
    bonus_with_savings_paused('1939')
    '''

    '''
    savings_passKyc_passTerms('1930')
    savings_passKyc_passTerms('1931')
    savings_passKyc_passTerms('1932')
    savings_passKyc_passTerms('1933')
    savings_passKyc_passTerms('1934')
    savings_passKyc_passTerms('1935')
    savings_passKyc_passTerms('1936')
    savings_passKyc_passTerms('1937')
    savings_passKyc_passTerms('1938')
    savings_passKyc_passTerms('1939')
    '''


    #################################
    # failed state: active users

    '''
    reset_savings_tile('1945')
    reset_savings_tile('1946')
    reset_savings_tile('1947')
    reset_savings_tile('1948')
    reset_savings_tile('1949')
    '''

    '''
    bonus_with_savings('1945')
    bonus_with_savings('1946')
    bonus_with_savings('1947')
    bonus_with_savings('1948')
    bonus_with_savings('1949')
    '''

    '''
    savings_failKyc_passTerms('1945')
    savings_failKyc_passTerms('1946')
    savings_failKyc_passTerms('1947')
    savings_failKyc_passTerms('1948')
    savings_failKyc_passTerms('1949')
    '''

    #################################
    # failed state: paused users

    '''
    reset_savings_tile('1950')
    reset_savings_tile('1951')
    reset_savings_tile('1952')
    reset_savings_tile('1953')
    reset_savings_tile('1954')
    '''

    '''
    bonus_with_savings_paused('1950')
    bonus_with_savings_paused('1951')
    bonus_with_savings_paused('1952')
    bonus_with_savings_paused('1953')
    bonus_with_savings_paused('1954')
    '''

    '''
    savings_failKyc_passTerms('1950')
    savings_failKyc_passTerms('1951')
    savings_failKyc_passTerms('1952')
    savings_failKyc_passTerms('1953')
    savings_failKyc_passTerms('1954')
    '''