#!/usr/bin/python2
# coding=utf-8
print 'Content-type: application/rss+xml\r\n\r'

from feedformatter import Feed
import datetime
import time
try:
    import urllib2
    PY2 = True
except ImportError:
    import requests
    PY2 = False

def findSection(text, start, end, includeStart = False, includeEnd = False):
    startIndex = text.find(start)
    if not includeStart:
        startIndex = startIndex + len(start)

    endIndex = text.find(end, startIndex)
    if includeEnd:
        endIndex = endIndex + len(end)

    return text[startIndex:endIndex]

def getData(url):
    if PY2:
        html = urllib2.urlopen(url).read()
    else:
        html = requests.get(url).text

    result = {}

    section = findSection(html, '<tbody class="style5">', '</table>')
    imageHtml = findSection(section, '<img', '>')
    
    result['dateFormatted'] = findSection(section, '<nobr>', ': </nobr>').strip()
    result['imageUrl'] = 'http://sinfest.net/' + findSection(imageHtml, 'src="', '"')
    result['date'] = findSection(imageHtml, 'btphp/comics/', '.gif')
    result['title'] = findSection(imageHtml, 'alt="', '"')
    result['url'] = 'http://sinfest.net/view.php?date=%s' % (result['date'])

    # sinfest no longer uses Project Wonderful and new ads don't seem to have a noscript section
    result['ad'] = ''

    return result

try:
    todaysSinfest = getData('http://sinfest.net/')
except Exception as e:
    print(e)
    today = datetime.date.today()
    todaysSinfest = {'title': 'could not fetch', 'url': '', 'imageUrl': '',
        'dateFormatted': today.strftime('%d %b %Y'),
        'date': today.strftime('%Y-%m-%d') }

# Create the feed.
feed = Feed()

# Set the feed/channel level properties.
feed.feed['title'] = 'Sinfest RSS'
feed.feed['link'] = 'http://www.sinfest.net'
feed.feed['author'] = 'Tatsuya Ishida'
feed.feed['description'] = 'RSS feed for Sinfest'
# Suggest checking every 12 hours. Normally content will update every 24 hours.
# This is an attempt to tell clients there's no point checking the feed
# every 5 minutes - it's not a big deal load-wise, but it is pointless.
feed.feed['ttl'] = '720'

# Create an item.
# For this basic feed, I'll only include the latest comic.
item = {}
item['link'] = todaysSinfest['url']
item['guid'] = todaysSinfest['date']
item["pubDate"] = time.localtime()
item['title'] = 'Sinfest for %s: %s' % (todaysSinfest['dateFormatted'], todaysSinfest['title'])
if todaysSinfest['imageUrl'] != '':
    item['summary'] = '<img src="%s" /><br/><br/>%s' % (todaysSinfest['imageUrl'], todaysSinfest['ad'])
else:
    item['summary'] = 'image not found'

# Add item to feed.
feed.items.append(item)
print feed.format_rss2_string()
