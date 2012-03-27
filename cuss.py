#CUSS. Css Unused SelectorS

import sys
import os
import re
from HTMLParser import HTMLParser

path = "./"
if(len(sys.argv) > 1):
	path = sys.argv[1]

folderfiles = os.listdir(path);

fileAttrs = ["href"];
checkTags = ["style"];
checkAttrs = ["id", "class"]

class cussParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print tag + " : " + str(attrs) 

def parseCSSFile(feed):
	newfeed = re.sub(r'\{.*?\}','', feed, 0,  re.DOTALL)
	print newfeed

for fname in folderfiles:
	if(".css" in fname):
		cf = open(os.path.join(path, fname), 'r')
		parseCSSFile(cf.read());


#index_f = open(path, 'r')
#parser = cussParser()
#parser.feed(index_f.read())
