#CUSS. Css Unused SelectorS

import sys
import os
import re
from HTMLParser import HTMLParser

#delimiters
delimiters = ['+','.','#','&','[']
consumers = ['+','&']

#splits the string but does not consume anything that is not also in the consume list
def splitmulti(string, delimit, consume):
	returnList = []
	liststr = ""
	for s in string:
		if(s in delimit):
			if(liststr != ""):
				returnList.append(liststr)
			liststr = ""
		if(s not in consume):
			liststr+= s
			
	returnList.append(liststr)
	return returnList
			

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
		feed = self.remove_replace(feed)
		#split the file into individual tags (the previous function replaced the css delimiters with our own)
		self.tags = feed.split("&")
		#cleans the tags of any psudo selectors
		self.clean_tags()	
		#print tags
		self.tags_to_set()	
		print self.create_tag_hash()

	def tags_to_set(self):
		self.tag_list = []
		for tag in self.tags:
			split_tag = splitmulti(tag, delimiters, consumers)
			self.tag_list.append(split_tag)
		self.tag_list = filter(None, self.tag_list)
		return self.tag_list	
	
	def create_tag_hash(self):
		self.tagmap = {}
		for i in range(len(self.tag_list)):
			tag = self.tag_list[i]
			for t in tag:
				if not t in self.tagmap:
					self.tagmap[t] = []
				self.tagmap[t].append(i)
		return self.tagmap

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
		newfeed = re.sub('//.*?\n|/\*.*?\*/|\*', '', feed, 0, re.DOTALL)
		newfeed = re.sub('\{.*?\}','&', newfeed, 0,  re.DOTALL)
		newfeed = re.sub('\+', '&', newfeed) #Because css allows + to work the same way as writing a new selector we simply pretend that its new selector.		
		#replace all whitespace with a plus symbol
		newfeed = re.sub(r'\s+', '+', newfeed, 0, re.MULTILINE)
		#remove any intances of the plus symbol interacting with the ampersand
		newfeed = re.sub("\+&\+|\+&|&\+|,\+", "&", newfeed)
		return newfeed


	def clean_tags(self):
		newtags = []
		for tag in self.tags:
			tag = re.sub('\*', '', tag)
			tag = re.sub('(?<=\w)\#(?=\w)', "&#", tag) #Will replace any "h1#id" with an &. 
			tag = re.sub('(?<=\w)\.(?=\w)', "&.", tag) #Will replace any "h1.id" with an &. 
			tag = re.sub('(?<=\w)\+?(?=\[)', "&", tag) #Will replace any "h1[attr=attrib]" with an &
			tag = re.sub('\:.*', '', tag)
			if(tag != ''):
				newtags.append(tag)
		newtags = sorted(set(newtags))
		self.tags = newtags
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

