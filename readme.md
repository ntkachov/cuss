#Cuss.py 
##The Unused CSS Selector Scanner


##Progress: 
Cuss is currently done. It parses out all css and html and traverses the directory tree properly with an option of which directories to exclude.

####Todo:
Add better directory exclusion options. Maybe a [-noparse] or [-n] option.

##Install:
Cuss neds python and PyQuery installed in order to run.
You can obtain PyQuery by running 

	pip install PyQuery

or 
	
	easy_install PyQuery

Chances are you will also need to install lxml to your system in order for pyquery to install.

	apt-get install libxml2
	apt-get install libxsit


##Usage:

	python cuss.py [./relative/path/to/www/ := .] [./relative/path/to/noparse := NONE]

Cuss requires a relative path to the root directory of the html. It will automatically scan for .css and .html files within the directory and its children.

	python cuss.py ../relative/path/to/www

If no path is provided cuss will assume it is in the root directory of the site.

A noparse file can be provided that will list directories that should not be scanned.
A simple noparse file would look like this

	/build
	/js
	/xml/build

This would exlude these directories in the walking of the directory tree. Thus any subdirectories inside these will not be scanned.



