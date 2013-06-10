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
		self.editingEntry=None
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
		self.mEntryList = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer1.Add( self.mEntryList, 1, wx.ALL|wx.EXPAND, 5 )
		self.mEntryDisplay = wx.html.HtmlWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		bSizer1.Add( self.mEntryDisplay, 2, wx.ALL|wx.EXPAND, 5 )
		self.mEntryNew = wx.Button( self, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 1 )
		self.mEntryEdit = wx.Button( self, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.DefaultSize, 1 )
		self.mEntryDelete = wx.Button( self, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.DefaultSize, 1 )
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		bSizer2.Add( self.mEntryNew, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer2.Add( self.mEntryEdit, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer2.Add( self.mEntryDelete, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer1.Add(bSizer2,0,wx.ALL,5)
		self.SetSizer( bSizer1 )
		self.Layout()
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.mEntryList.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onItemSelect )
		self.mEntryNew.Bind( wx.EVT_BUTTON, self.onNew )
		self.mEntryEdit.Bind( wx.EVT_BUTTON, self.onEdit )
		self.mEntryDelete.Bind( wx.EVT_BUTTON, self.onDelete )
	
	def __del__( self ):
		pass

	def showEditWindow(self,entry):
		#create dialog
		self.editingEntry=entry
		self.editDialog=wx.Dialog(self,id = wx.ID_ANY, title = "Edit Entry", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		#create widgets
		self.txtEntry = wx.TextCtrl( self.editDialog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		self.txtEntry.SetMinSize( wx.Size( 400,200 ) )
		self.txtTags = wx.TextCtrl( self.editDialog, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.chkStarred = wx.CheckBox( self.editDialog, wx.ID_ANY, u"Starred", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sdbSizer1OK = wx.Button( self.editDialog, wx.ID_OK )
		self.m_sdbSizer1Cancel = wx.Button( self.editDialog, wx.ID_CANCEL )

		#create sizers
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		m_sdbSizer1 = wx.StdDialogButtonSizer()

		#add widgets
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		bSizer1.Add( self.txtEntry, 0, wx.ALL, 5 )
		bSizer2.Add( self.txtTags, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer2.Add( self.chkStarred, 0, wx.ALL, 5 )
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		bSizer1.Add( m_sdbSizer1, 1, wx.EXPAND, 5 )

		#setlayout
		self.editDialog.SetSizer( bSizer1 )
		self.editDialog.Layout()
		bSizer1.Fit( self.editDialog )

		#setValues
		if entry.getEntryText(): self.txtEntry.SetValue(entry.getEntryText())
		if entry.getEntryTags(): self.txtTags.SetValue(','.join(entry.getEntryTags()))
		if entry.getEntryStarred(): self.chkStarred.SetValue(True)

		#bind events
		self.m_sdbSizer1OK.Bind( wx.EVT_BUTTON, self.onEditSave )
		self.m_sdbSizer1Cancel.Bind( wx.EVT_BUTTON, self.onEditCancel )

		self.editDialog.ShowModal()

	def onItemSelect(self,event):
		entryID=self.mEntryList.GetItem(event.m_itemIndex,2).GetText()
		selectedEntry=self.journal.getEntryByID(entryID)
		html=markdown.markdown(selectedEntry.getEntryText())
		self.mEntryDisplay.SetPage(html)

	def getSelectedEntryID(self):
		idx=self.mEntryList.GetFirstSelected()
		if(idx>0):
			return self.mEntryList.GetItem(idx,2).GetText()
		else:
			return None

	def onEdit(self,event):
		entryid=self.getSelectedEntryID()
		if entryid:
			entry=self.journal.getEntryByID(entryid)
			self.showEditWindow(entry)

	def onNew(self,event):
		entry=DayOneEntry()
		self.showEditWindow(entry)

	def onEditSave(self,event):
		self.editingEntry.setEntryText(self.txtEntry.GetValue())
		self.editingEntry.setEntryStarred(self.chkStarred.GetValue())
		if self.txtTags.GetValue():
			self.editingEntry.setEntryTags(self.txtTags.GetValue().split(','))

		self.journal.saveEntry(self.editingEntry)
		self.populateListCtrl() #reload list
		self.editingEntry=None
		self.closeEditDialog()

	def onEditCancel(self,event):
		self.closeEditDialog()
		self.editingEntry=None

	def closeEditDialog(self):
		self.editDialog.EndModal(0)
		self.editDialog.Destroy()

	def onDelete(self,event):
		entryid=self.getSelectedEntryID()
		if entryid:
			entry=self.journal.getEntryByID(entryid)
			self.journal.deleteEntry(entry)
			self.populateListCtrl()

if __name__ == '__main__':
	app=wx.App()
	myApp=libDayOneEx(None)
	myApp.Show()
	app.MainLoop()