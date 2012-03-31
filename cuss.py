#CUSS. Css Unused SelectorS

import sys
import os
import re
from HTMLParser import HTMLParser

#delimiters
delimiters = ['+','.','#','&'];
consumers = ['+','&'];

def splitmulti(string, delimit, consume):
	returnList = []
	liststr = "";
	for s in string:
		if(s in delimit):
			if(liststr != ""):
				returnList.append(liststr)
			liststr = "";
		if(s not in consume):
			liststr+= s
			
	return returnList;
			

#Class to store everything propperly
class CSSFile:
	def __init__(self, filename, feed):
		self.file_name = filename
		self.text = feed
		
		#check for matched parens. (Unmatched parens will cause errors)
		if(self.checkParens(feed) != 0):
			print ("Unmatched brackets in css file: " + filename)
			exit()	
		
		#get rid of @media. Nested brackets make regex harder. 
		feed = self.remove_media(feed)	
		#remove comments, braces, and provide delimiters "&" and "+"
		feed = self.remove_replace(feed);
		#split the file into individual tags (the previous function replaced the css delimiters with our own)
		tags = feed.split("&")
		#cleans the tags of any psudo selectors
		tags = self.clean_tags(tags)	
		#print tags;
		self.create_tag_hash(tags)
	
	def create_tag_hash(self, tags):
		self.tagmap = {}
		for i in range(len(tags)):
			tag = tags[i]
			split_tag = splitmulti(tag,delimiters, consumers);
			for t in split_tag:
				print t
				if not t in self.tagmap:
					self.tagmap[t] = []
				self.tagmap[t].append(i)
			

	def checkParens(self, feed):
		#Count the difference between the number of opening brackets and closing brackets.
		parenCount = 0
		for c in feed:
			if(c == "{"):
				parenCount +=1
			elif(c == "}"):
				parenCount -=1
		return parenCount
			
	def remove_media(self, feed):
		newfeed = ""
		insert = True
		parencount = 0
		betweenbrackets = False
		for c in feed:
			if(c == '['):
				betweenbrackets = True
			elif(c == ']'):
				betweenbrackets = False

			if (not (betweenbrackets and re.match('\s', c))) :	#remove extra whitespace.
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
				elif(insert):
					newfeed += c
		return newfeed

	def remove_replace(self, feed):
		#remove Any comments and anything between brackets.
		newfeed = re.sub('//.*?\n|/\*.*?\*/', '', feed, 0, re.DOTALL)
		newfeed = re.sub('\{.*?\}','&', newfeed, 0,  re.DOTALL)
		newfeed = re.sub('\+', '&', newfeed) #Because css allows + to work the same way as writing a new selector we simply pretend that its new selector.		
		#replace all whitespace with a plus symbol
		newfeed = re.sub(r'\s+', '+', newfeed, 0, re.MULTILINE)
		#remove any intances of the plus symbol interacting with the ampersand
		newfeed = re.sub("\+&\+|\+&|&\+|,\+", "&", newfeed)
		return newfeed


	def clean_tags(self, tags):
		newtags = []
		for tag in tags:
			tag = re.sub('\*', '', tag);
			tag = re.sub('(?<=\w)\#(?=\w)', "&#", tag) #Will replace any "h1#id" with an &. 
			tag = re.sub('(?<=\w)\.(?=\w)', "&.", tag) #Will replace any "h1.id" with an &. 
			tag = re.sub('(?<=\w)\+?(?=\[)', "&", tag) #Will replace any "h1[attr=attrib]" with an &
			if "[" in tag:
				tag = re.sub(r'\:.*|', '', tag)
			if(tag != ''):
				newtags.append(tag)
		newtags = sorted(set(newtags))
		return newtags
	
#HTML parsing and checking.

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
			CSSFile(fname, cf.read())
			


main()

