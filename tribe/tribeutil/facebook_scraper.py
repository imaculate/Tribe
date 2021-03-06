import csv
import re
import time
from datetime import datetime
from datetime import timedelta
from urllib.request import Request, urlopen
from pandas import json

def request_until_succeed(url):
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.now()))
            print("Retrying.")

    return response.read()

# Needed to write tricky unicode correctly to csv


def unicode_decode(text):
    try:
        return text.encode('utf-8', errors='ignore').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8', errors='ignore')


def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=message,link,created_time,status_type,name,id," + \
        "comments.limit(5).summary(true),shares,reactions" + \
        ".limit(5).summary(true),from"
    url = base_url + fields

    return url


def getReactionsForStatuses(base_url):

    reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
    reactions_dict = {}   # dict of {status_id: tuple<6>}

    for reaction_type in reaction_types:
        fields = "&fields=reactions.type({}).limit(5).summary(total_count)".format(
            reaction_type.upper())

        url = base_url + fields

        data = json.loads(request_until_succeed(url))['data']

        data_processed = set()  # set() removes rare duplicates in statuses
        for status in data:
            id = status['id']
            count = status['reactions']['summary']['total_count']
            data_processed.add((id, count))

        for id, count in data_processed:
            if id in reactions_dict:
                reactions_dict[id] = reactions_dict[id] + (count,)
            else:
                reactions_dict[id] = (count,)

    return reactions_dict


def processFacebookPageFeedStatus(status):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first

    status_id = status['id']
    status_type = '' if 'type' not in status else status['type']

    status_message = '' if 'message' not in status else \
        unicode_decode(status['message'])
    link_name = '' if 'name' not in status else \
        unicode_decode(status['name'])
    status_link = '' if 'link' not in status else \
        unicode_decode(status['link'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.strptime(
        status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
        timedelta(hours=-5)  # EST
    status_published = status_published.strftime(
        '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs
    status_author = unicode_decode(status['from']['name'])

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
        status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
        status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else status['shares']['count']

    return (status_id, status_message, status_author, link_name, status_type,
            status_link, status_published, num_reactions, num_comments, num_shares)

def is_group_public(access_token, group_id):
    url = "https://graph.facebook.com/v2.10/" + group_id + "?access_token={}".format(access_token)+ "&fields=privacy"
    req = Request(url)
    try:
        response = urlopen(req)
        if response.getcode() == 200:
            group_info = json.loads(response.read())
            return group_info['privacy'] == 'OPEN'
    except Exception as e:
        #traceback.print_tb(e.__traceback__)
        return False #assuming all errors will be due to permission errors


def scrapeFacebookPageFeedStatus(group_id, access_token, since_date, until_date,format='json'):
    filename = '{}_facebook_statuses_{}'.format(group_id, int(datetime.now().timestamp())) + "."+ format
    f = open(filename, 'w', encoding='utf-8')
    w = None
    if format == 'csv':
        w = csv.writer(f)
        w.writerow(["status_id", "status_message", "status_author", "link_name",
                        "status_type", "status_link", "status_published",
                        "num_reactions", "num_comments", "num_shares", "num_likes",
                        "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys"])
    has_next_page = True
    num_processed = 0   # keep a count on how many we've processed
    scrape_starttime = datetime.now()

    # /feed endpoint pagenates througn an `until` and `paging` parameters
    paging = ''
    base = "https://graph.facebook.com/v2.10"
    node = "/{}/feed".format(group_id)
    parameters = "/?limit={}&access_token={}".format(100, access_token)
    since = "&since={}".format(since_date) if since_date \
                                              is not '' else ''
    until = "&until={}".format(until_date) if until_date \
                                              is not '' else ''

    print("Scraping {} Facebook Group: {}\n".format(
        group_id, scrape_starttime))

    while has_next_page:
        until = '' if until is '' else "&until={}".format(until)
        paging = '' if paging is '' else "&__paging_token={}".format(paging)
        base_url = base + node + parameters + since + until + paging

        url = getFacebookPageFeedUrl(base_url)
        statuses = json.loads(request_until_succeed(url))

        if format == 'json':
            json.dump(statuses, f, ensure_ascii=False)
            num_processed += len(statuses['data'])
        else:
            reactions = getReactionsForStatuses(base_url)
            for status in statuses['data']:
                # Ensure it is a status with the expected metadata
                status_data = processFacebookPageFeedStatus(status)

                if 'reactions' in status:
                    reactions_data = reactions[status_data[0]]
                    status_data = status_data + reactions_data #concatenate the data

                w.writerow(status_data)
                num_processed += 1

        if num_processed % 100 == 0:
            print("{} Statuses Processed: {}".format
                  (num_processed, datetime.now()))

        if 'paging' in statuses:
            next_url = statuses['paging']['next']
            until = re.search('until=([0-9]*?)(&|$)', next_url).group(1)
            paging = re.search(
                '__paging_token=(.*?)(&|$)', next_url).group(1)

        else:
            has_next_page = False
    print("\nDone!\n{} Statuses Processed in {}".format(
        num_processed, datetime.now() - scrape_starttime))

    f.close()

if __name__ == '__main__':
    print("scrapper")