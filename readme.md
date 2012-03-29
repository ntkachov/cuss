#Cuss.py 
##The Unused CSS Selector Scanner


##Progress: 
Cuss currently only parses out all of your selectors, ignoring children selectors. It does not parse the actuall HTML yet.

####Todo:
Add support for child selectors and attribute attribute tags to the collective ttag.eg:

	header #id [data=color] { color:blue }

Store the origin file of each selector and check the HTML to see if it links to the origin file. This is in case two files use the same class name but not both of the classes are used in the HTML files that actually link to them.

Scan the directories properly. Right now the dir scanning code is crap.

Actually scan the HTML and do the linking.

##Usage:
Cuss requires a relative path to the root directory of the html. It will automatically can for relative .css and .htmt.

	python cuss.py ../relative/path/to/www

If no path is provided cuss will assume it is in the root directory of the site.





