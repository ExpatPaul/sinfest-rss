#!/usr/bin/env python
# coding=utf-8

from feedformatter import Feed
import datetime
import time
import urllib2

def findSection(text, start, end, includeStart = False, includeEnd = False):
    startIndex = text.find(start)
    if not includeStart:
        startIndex = startIndex + len(start)

    endIndex = text.find(end, startIndex)
    if includeEnd:
        endIndex = endIndex + len(end)

    return text[startIndex:endIndex]

def getData(url):
    html = urllib2.urlopen(url).read()

    result = {}

    section = findSection(html, '<tbody class="style5">', '</table>')
    imageHtml = findSection(section, '<img', '>')
    
    result['dateFormatted'] = findSection(section, '<nobr>', ': </nobr>').strip()
    result['imageUrl'] = 'http://sinfest.net/' + findSection(imageHtml, 'src="', '"')
    result['date'] = findSection(imageHtml, 'btphp/comics/', '.gif')
    result['title'] = findSection(imageHtml, 'alt="', '"')
    result['url'] = 'http://sinfest.net/view.php?date=%s' % (result['date'])

    return result

try:
    todaysSinfest = getData('http://sinfest.net/')
except:
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

# Create an item.
# For this basic feed, I'll only include the latest comic.
item = {}
item['link'] = todaysSinfest['url']
item['guid'] = todaysSinfest['date']
item["pubDate"] = time.localtime()
item['title'] = 'Sinfest for %s: %s' % (todaysSinfest['dateFormatted'], todaysSinfest['title'])
if todaysSinfest['imageUrl'] != '':
    item['summary'] = '<img src="%s" />' % (todaysSinfest['imageUrl'])
else:
    item['summary'] = 'image not found'

# Add item to feed.
feed.items.append(item)

# Save the feed to a file.
feed.format_rss2_file('rss2.xml')

