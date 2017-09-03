import sys
import os
from datetime import datetime
from datetime import timedelta
from dateutil import parser
import argparse

#PACKAGE_PARENT = '..'
#SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
#sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


from tribe.tribeutil.facebook_scraper import scrapeFacebookPageFeedStatus
from tribe.tribeutil.facebook_scraper import is_group_public

valid_formats = ['json', 'csv']
NUM_ID_TRIALS = 3
this = sys.modules[__name__]

def get_access_token():
    f = open(os.path.join(os.path.dirname(__file__),'app_secrets'), 'r')
    app_id = f.readline().strip("\n")
    app_secret = f.readline().strip("\n")
    return app_id + "|"+ app_secret

def valid_group_id(group_id):
    return group_id.isdigit()

def valid_date_format(date):
    valid = False
    try:
        parser.parse(date)
        valid = True
    except ValueError:
        pass
    return valid

def parse_cli_parameters():
    parser = argparse.ArgumentParser(description='Tribe app')

    parser.add_argument('-g', action="store", default='')
    parser.add_argument('-s', action="store", default='')
    parser.add_argument('-e', action="store", default='')
    parser.add_argument('-f', action="store", default='')

    results = parser.parse_args()

    group_id = results.g
    if not valid_group_id(group_id):
        print("The format of the ID you entered doesn't look right, it is a number")
        sys.exit(-1)

    if not is_group_public(this.access_token, group_id):
        print("Looks like this group is not public, only public groups are currently supported")
        sys.exit(-1)
    start_date = '{:%Y-%m-%d}'.format(datetime.utcnow().date() - timedelta(days=2))
    if valid_date_format(results.s):
        start_date = results.s

    end_date = '{:%Y-%m-%d}'.format(datetime.utcnow().date())
    if valid_date_format(results.s):
        end_date = results.e

    format = 'json'
    if results.f in valid_formats:
        format = results.f
    return (group_id, start_date, end_date, format)


def converse():
    group_id = input("Enter group ID( a number):").strip("\"\'")
    trial = 1
    while(not valid_group_id(group_id) and trial < NUM_ID_TRIALS):
        group_id = input("The format of the ID you entered doesn't look right \n, Please enter group id( a number):")
        trial+=1

    if not valid_group_id(group_id):
        print("The group id you entered is invalid")
        sys.exit(-1)

    if not is_group_public(this.access_token, group_id):
        print("Looks like this group is not public, only public groups are currently supported")
        sys.exit(-1)

    start_date = input("You would like updates since what date(YYYY-MM-DD)?\nThe default is 2 days ago)")
    if not valid_date_format(start_date):
        start_date = '{:%Y-%m-%d}'.format(datetime.utcnow().date() - timedelta(days=2))

    end_date = input("You would like updates until what date (YYYY-MM-DD)?\nThe default is today")
    if not valid_date_format(end_date):
        end_date = '{:%Y-%m-%d}'.format(datetime.utcnow().date())
    format = input('What format for the data? Default is json(json/csv)')
    if format not in valid_formats:
        format = 'json'
    return (group_id, start_date, end_date, format)

def get_posts():
    this.access_token = get_access_token()
    if(len(sys.argv) > 1):
        (group_id, since_date, until_date, format) = parse_cli_parameters()
    else:
        (group_id, since_date, until_date, format) = converse()
    scrapeFacebookPageFeedStatus(group_id, this.access_token, since_date, until_date, format)

