#CUSS. Css Unused SelectorS

import sys
import os
import re
from HTMLParser import HTMLParser

#CSS Parsing 
def parseCSSFile(filename, feed):
	#check for matched parens. (Unmatched parens will cause errors)
	if(checkParens(feed) != 0):
		print ("Unmatched brackets in css file: " + filename)
		exit()	
	
	#get rid of @media. Nested brackets make regex harder. 
	feed = removeMedia(feed)	

	#remove Any comments and anything between brackets.
	newfeed = re.sub('//.*?\n|/\*.*?\*/', '', feed, 0, re.DOTALL)
	newfeed = re.sub('\{.*?\}','&', newfeed, 0,  re.DOTALL)
	newfeed = re.sub(r'\s+', '+', newfeed, 0, re.MULTILINE)
	print newfeed
	tags = newfeed.split("&")
	#tags = sortTags(tags)	
	#attributes = splitAttrs(tags);

def checkParens(feed):
	parenCount = 0
	for c in feed:
		if(c == "{"):
			parenCount +=1
		elif(c == "}"):
			parenCount -=1
	return parenCount
		
def removeMedia(feed):
	newfeed = ""
	insert = True
	parencount = 0
	betweenbrackets = False
	for c in feed:
		if(c == '['):
			betweenbrackets = True;
		elif(c == ']'):
			betweenbrackets = False;
		if (not (betweenbrackets and re.match('\s', c))) :	
			if(c == "@"):
				insert = False
			elif(not insert and c == "{"):
				insert = True
				parencount += 1
			elif(insert and parencount > 0):
				if( c == "{" ):
					parencount +=1
				elif( c == "}" ):
					parencount -=1
				if(parencount != 0):
					newfeed += c
			else:
				if(insert):
					newfeed += c
	return newfeed

def sortTags(tags):
	newtags = []
	for tag in tags:
		if "[" in tag:
			tag = re.sub(r'\:.*', '', tag)
			tag = re.sub(',','', tag)
			newtags.append(tag)
	newtags = sorted(set(newtags))
	return newtags

def splitAttrs(tags):
	attrs = {}
	for tag in tags:
		if('[' in tag):
		 	attr = re.findall('\[.*?\]', tag);
			origintag = tag[0: int(tag.find("["))];
			if origintag not in attrs:
				attrs[origintag] = [];
			attrs[origintag].append(attr)
	return attrs


#HTML parsing and checking.

fileAttrs = ["href"]
checkTags = ["style"]
checkAttrs = ["id", "class"]

class cussParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		print tag + " : " + str(attrs) 


#Program initialization
def main():
	path = "./"
	if(len(sys.argv) > 1):
		path = sys.argv[1]

	folderfiles = os.listdir(path)

	for fname in folderfiles:
		if(".css" in fname):
			cf = open(os.path.join(path, fname), 'r')
			parseCSSFile(fname, cf.read())


main()

