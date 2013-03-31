#!/usr/bin/env python
from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
from urlparse import urljoin,urlparse
import sys

pages_visited = []
startDomain = ""

def checkDead(url, fromUrl = ""):
  if url in pages_visited:
    return []
  pages_visited.append(url)
  if 'jpg' in url:
    return []
  print "Trying " + url
  try:
    soup = BeautifulSoup(urlopen(url).read())
    retval = []
    for link in soup.find_all('a'):
      if urlparse(url).netloc == startDomain:
        retval.extend(checkDead(urljoin(url, link.get('href')), url))
    return retval
  except HTTPError as e:
    return [(url, fromUrl, str(e.code))]
  except URLError as e:
    if 'mailto' in e.args[0]:
      return []
    return [(url, fromUrl, e.args)]


if __name__ == "__main__":
  startDomain = urlparse(sys.argv[1]).netloc
  deadLinks = checkDead(sys.argv[1])
  if len(deadLinks) > 0:
    for item in deadLinks:
      print "[%10s]:\t%50s\t=>\t%-50s" % (item[2], item[1], item[0])
  else:
    print "No dead links found!"
