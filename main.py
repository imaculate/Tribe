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
app_id = ''#read from secrets
app_secret = ''#read from secrets

if __name__ == '__main__':
    #token_handler = app_id + TokenHandler("160706031152243","f0419cf551c7cd6117057e884c93b05d")
    access_token = "160706031152243|EwZnMb_xw-3hG5TYddm07-TK0CY"#app_id + "|"+ app_secret
    scrapeFacebookPageFeedStatus(group_id, access_token, since_date, until_date)