#CUSS. Css Unused SelectorS

import sys
import os
import re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
from pyquery import PyQuery

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
		print self.tags

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
	
#HTML handle and checking
def html_init(fname, pq):
	src =  pq.find("link")
	for c in src:
		c = pq(c).attr("href")
		if(c in cssFiles):
			crosscheck_css(fname, pq, cssFiles[c])	
		else:
			print "in " +fname + ": " + c + " not found"

	

def crosscheck_css(fname, pq, css):
	for tag in css.tags:
		tag = re.sub('\+', ' ', tag)
		tag = re.sub('&', '', tag)
		if(str(pq(tag)) == ""):
			#print "in " +fname + ": " +tag + " is unused"
			if( tag not in usedTags):
				unusedTags[tag] = css.file_name
		else:
			if( tag in unusedTags ):
				del unusedTags[tag]
			usedTags.append(tag)
		
			

#Program initialization
cssFiles = {}
htmlFiles = []
unusedTags = {}
usedTags = []
noparse = []

def scan_files(path):
	folderfiles = os.listdir(path)

	for fname in folderfiles:
		if(fname[-4:] == ".css"):
			cf = open(os.path.join(path, fname), 'r')
			cssFiles[fname] = CSSFile(fname, cf.read())
		elif(fname[-5:] == ".html"):
			cf = open(os.path.join(path, fname),'r')
			pq = PyQuery(cf.read())
			htmlFiles.append({'name': fname, 'data': pq})

def get_dirs(path, noparse):
	folderlist = []
	
	dirlist = os.listdir(path)
	for fname in dirlist:
		dirt = os.path.join(path,fname)
		if(os.path.isdir(dirt) and dirt[1:] not in noparse and fname[0] != '.'):
			folderlist += get_dirs(dirt, noparse)
			folderlist.append(dirt)	
	return folderlist
			

def main():
	path = "./"
	if(len(sys.argv) > 1):
		path = sys.argv[1]
		if(len(sys.argv) > 2):
			noparse = open(sys.argv[2], 'r').read().split("\n")
			noparse = filter(None, noparse)
			print noparse
				

	folderList = get_dirs(path, noparse)
	folderList.append(path)
	for f in folderList:
		scan_files(f)

	for html in htmlFiles:
		html_init(html['name'], html['data'])
	for tag in unusedTags:
		print "in " + unusedTags[tag] + ": " + tag + "is unused"	


main()

