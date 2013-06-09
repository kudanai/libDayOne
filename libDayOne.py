#!/usr/bin/env python

# libDayOne
# 2013 - @kudanai

from uuid import uuid4
from datetime import datetime
from glob import glob
import plistlib
import os

__author__="@kudanai"
__version__="0.1"

class DayOneJournal():
	"class to represent an entire DayOne Journal"
	#todo:also read security.plist

	def __init__(self,journalpath):
		self.entries=[]
		self.photos=[]  #todo:load photos and add method to set entry photo
		if os.path.exists(journalpath):
			self.jpath=journalpath
			self.reloadEntries()
		else:
			raise IOError("error reading from journal")

	def reloadEntries(self):
		for filename in glob(os.path.join(self.jpath,'entries',"*.doentry")):
			self.entries.append(DayOneEntry(filename))

	def getEntryIDs(self):
		"returns a list of entry IDs"
		entryIDS=[]
		for entry in self.entries:
			entryIDS.append(entry.getEntryID())
		return entryIDS

	def getEntries(self):
		"returns all DayOneEntry objects in the journal"
		return self.entries

	#I guess the workflow for modifying an entry would be to
	# 1. getEntryByID we want to modify
	# 2. saveEntry (should overwrite the old plist as needed)
	# 3. reloadEntries
	#
	# this is a bit expensive, but unless journal is very large
	# this shouldn't be a problem
	# TODO: improve this

	def getEntryByID(self,entryID):
		"returns a DayOneEntry corrosponding to the entryID"
		for entry in self.entries: #eek!
			if entry.getEntryID()==entryID:
				return entry
		return None		

	def saveEntry(self,entry):
		"saves the entry to the Journal entry path"
		if isinstance(entry,DayOneEntry):
			entry.writeEntryToFile(os.path.join(self.jpath,'entries'))
		else:
			raise IOError('invalid entry object')


class DayOneEntry():
	"class to represent a DayOne journal entry"

	def __init__(self,filename=None):
		"if filename is given, read from file. Otherwise create a new entry"
		self.entry = {}
		if filename:
			self.entry=plistlib.readPlist(filename);
		else:
			self.__initnewentry()

	def __initnewentry(self):
		"initialize a blank entry with minimum stuff"
		self.entry={"UUID":uuid4().hex.upper(),
					"Creation Date":datetime.utcnow(),
					"Starred":False,
					"Entry Text":""}

	def getEntryDict(self):
		"returns the entry dictionary"
		return self.entry

	def getEntryID(self):
		"returns the UUID associated with the entry"
		return self.entry["UUID"]

	def getEntryText(self):
		"returns the entry text"
		return self.entry["Entry Text"]

	def getEntryDate(self):
		"returns a datetime object of the creation date"
		return self.entry.get["Creation Date"]

	def getEntryTags(self):
		"returns the entry tags"
		#note-using dict.get() here because other tags are set
		#on init anyway.
		return self.entry.get("Tags")

	def setEntryText(self,entrytext):
		"call to set the entry text"
		if entrytext:
			self.entry["Entry Text"]=entrytext

	def setEntryTags(self,entrytags):
		"accepts a list, or comma seperated string to set as tags"
		if isinstance(entrytags,list):
			self.entry["Tags"]=entrytags
		else:
			self.entry["Tags"]=entrytags.split(',')

	def setEntryStarred(self,flag):
		"boolean true/false to set entry as starred or not"
		if isinstance(flag,bool):
			self.entry["Starred"]=flag
		else:
			self.entry["Starred"]=False
		
	def writeEntryToFile(self,basedir):
		"write the entry to a directory with entry_id.doentry as the file name"
		outfile=os.path.join(basedir,"%s.doentry"%self.getEntryID())
		plistlib.writePlist(self.entry,outfile)