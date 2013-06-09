#!/usr/bin/env python

import wx
import markdown
from libDayOne import DayOneEntry,DayOneJournal
import wx.html
import os

conf_DOJpath=os.path.expanduser('~/Documents/Dropbox/Apps/Day One/Journal.dayone')

class libDayOneEx ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 620,472 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.createWindow()
		self.journal = DayOneJournal(conf_DOJpath)
		self.populateListCtrl()

	def populateListCtrl(self):
		self.mEntryList.ClearAll()
		self.mEntryList.InsertColumn(0,"Entry Summary")
		self.mEntryList.InsertColumn(1,"Entry Date")
		self.mEntryList.InsertColumn(2,"UUID")

		self.mEntryList.SetColumnWidth(0, 400)
		self.mEntryList.SetColumnWidth(1, 150)
		self.mEntryList.SetColumnWidth(2, 0); #hide the UUID column

		idx=0
		for entry in self.journal.getEntries():
			self.mEntryList.InsertStringItem(idx,"text")
			self.mEntryList.SetStringItem(idx,0,entry.getEntryText().strip()[0:40]+"...")
			self.mEntryList.SetStringItem(idx,1,entry.getEntryDate().strftime('%Y/%m/%d %H:%M:%S'))
			self.mEntryList.SetStringItem(idx,2,entry.getEntryID())
			idx+=1


	def createWindow(self):
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		self.mEntryList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer1.Add( self.mEntryList, 1, wx.ALL|wx.EXPAND, 5 )
		self.mEntryDisplay = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		bSizer1.Add( self.mEntryDisplay, 2, wx.ALL|wx.EXPAND, 5 )
		self.SetSizer( bSizer1 )
		self.Layout()
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.mEntryList.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onItemSelect )
	
	def __del__( self ):
		pass

	def onItemSelect(self,event):
		entryID=self.mEntryList.GetItem(event.m_itemIndex,2).GetText()
		selectedEntry=self.journal.getEntryByID(entryID)
		html=markdown.markdown(selectedEntry.getEntryText())
		self.mEntryDisplay.SetPage(html)

if __name__ == '__main__':
	app=wx.App()
	myApp=libDayOneEx(None)
	myApp.Show()
	app.MainLoop()