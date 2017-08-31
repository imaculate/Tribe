import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

  
from tribeutil.facebook_scraper import scrapeFacebookPageFeedStatus
from tribeutil.server_handler import TokenHandler

group_id = "1384252878496456"

# input date formatted as YYYY-MM-DD
since_date = "2017-08-25"
until_date = "2017-08-28"


def get_access_token():
    f = open('app_secrets', 'r')
    app_id = f.readline().strip("\n")
    app_secret = f.readline().strip("\n")
    return app_id + "|"+ app_secret

if __name__ == '__main__':
    access_token = get_access_token()
    scrapeFacebookPageFeedStatus(group_id, access_token, since_date, until_date)