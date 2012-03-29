#CUSS. Css Unused SelectorS

import sys
import os
import re
from HTMLParser import HTMLParser

#Class to store everything propperly
class CSSFile:
	def __init__(self, filename, feed):
		self.file_name = filename
		self.child_tree = {}
		self.selector_mark = {}	

		#check for matched parens. (Unmatched parens will cause errors)
		if(checkParens(feed) != 0):
			print ("Unmatched brackets in css file: " + filename)
			exit()	
		
		#get rid of @media. Nested brackets make regex harder. 
		feed = removeMedia(feed)	

		#remove Any comments and anything between brackets.
		newfeed = re.sub('//.*?\n|/\*.*?\*/', '', feed, 0, re.DOTALL)
		newfeed = re.sub('\{.*?\}','&', newfeed, 0,  re.DOTALL)
		#replace all whitespace with a plus symbol
		newfeed = re.sub(r'\s+', '+', newfeed, 0, re.MULTILINE)
		#remove any intances of the plus symbol interacting with the ampersand
		newfeed = re.sub("\+&\+|\+&|&\+|,\+|\+\+\+", "&", newfeed)
		#print newfeed
		tags = newfeed.split("&")
		#print tags
		tags = sortTags(tags)	
		#print tags
		attributes = splitAttrs(tags)
		createTagTree(attributes);
		#print attributes

def checkParens(feed):
	#Count the difference between the number of opening brackets and closing brackets.
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
			else:
				if(insert):
					newfeed += c
	return newfeed

def sortTags(tags):
	newtags = []
	for tag in tags:
		tag = re.sub('\*', '', tag);
		tag = re.sub('(?<=\w)\#(?=\w)', "&#", tag) #Will replace any "h1.class" or "h1#id" with an &. 
		tag = re.sub('(?<=\w)\.(?=\w)', "&.", tag) #Will replace any "h1.class" or "h1#id" with an &. 
		if "[" in tag:
			tag = re.sub(r'\:.*|', '', tag)
		newtags.append(tag)
	newtags = sorted(set(newtags))
	return newtags

def splitAttrs(tags):
	attrs = {}
	for tag in tags:
		origintag = tag
		if('[' in tag):
		 	attr = re.findall('\[.*?\]', tag)
			origintag = tag[0: int(tag.find("["))]
			if(origintag[-1] == "+"): origintag = origintag[0:-1]
			if origintag not in attrs:
				attrs[origintag] = []
			attrs[origintag] = attr
		else:
			attrs[origintag] = ''
	return attrs

def createTagTree(attrs):
	def treeType(split, s_tree, tag, atts):
			children = t.split(split)
			node = s_tree
			for c in children:
				if(c in node):
					node = node[c]
				else:
					node[c] = {}
					node = node[c]
			for a in atts:
				node[a] = False;
			#s_tree =  dict(s_tree.items() + node.items())
			return s_tree 
		 
	childTree = {};
	selectorTree = {}
	selectorMark = {}
	for t in attrs: 
		selectorMark[t] = False
		if( "+" in t ): #handle child case
			childTree = treeType("+", childTree, t, attrs[t])
		if( "&" in t): #handle multi case
			selectorTree = treeType("&", selectorTree, t, attrs[t])	
	print attrs
	
	print childTree
	print selectorTree
	print selectorMark
			
				
					

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
			CSSFile(fname, cf.read())


main()

