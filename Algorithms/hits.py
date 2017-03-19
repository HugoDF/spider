import urllib, urllib2
import os, os.path
from textBased import search
from bs4 import BeautifulSoup

textBasedList = search("Python", "bbc")

topList = textBasedList[:10]

HITSList = []

for file in range(0, len(topList)):
	HITSList.append((0, topList[file][1]))
	sock = urllib.urlopen(topList[file][1])
	htmlSource = sock.read()
	sock.close()
	soup = BeautifulSoup(htmlSource, "lxml")
	for link in soup.findAll('a'):
		HITSList.append((0, link.get('href')))

print HITSList