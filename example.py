#!/usr/bin/env python

from tempfile import mkstemp
from libDayOne import DayOneEntry
import subprocess
import os

#basic configuration options
config = {"export_path":".",
		  "editor_cmd":"vi"}

def main():
	#create a blank entry
	et=DayOneEntry()
	et.setEntryText(getEntry())
	et.setEntryTags(["test tag","anarchy","dormatitis"])

	#write the entry to file if entry isn't..empty
	et.writeEntryToFile(config["export_path"])

def getEntry():
	#create a temporary file for edit
	#md format for markdown highlighting 
	f,path=mkstemp(suffix=".md")

	p=subprocess.Popen("%s %s"%(config["editor_cmd"],path),shell=True)
	p.wait()
	with open(path,"r") as fi:
		output=fi.read()

	#close and delete the file
	os.close(f)
	os.remove(path)
	return output

if __name__ == '__main__':
	main()