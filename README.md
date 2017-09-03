A desktop to retrieve posts on a facebook group (tribe).
It is intended to let users get content they really care about without other distractions from facebook.com
Built on Facebook Page Post Scraper(https://github.com/minimaxir/facebook-page-post-scraper) by @minimaxir

Usage
pip install tribe

>> tribe

For conversational input

or

>>tribe -g 1384252878496456 -s 2017-08-13 -e 2017-08-15 -f csv


1) -g (Group id) - required
2) -s (start date) -optional, default is 2 days
3) -e (end date) - optional, default is today
4) -f (format) - optional, default is json



To-do:
1) scrutinize error from public group check :permission code = 100
2) format comments csv

3) Future stretch goal after login is possible - private groups after users sign in, group id from group name


