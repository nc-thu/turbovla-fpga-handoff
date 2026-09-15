# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.11.5 | packaged by Anaconda, Inc. | (main, Sep 11 2023, 13:26:23) [MSC v.1916 64 bit (AMD64)]
# From type library '{00021A98-0000-0000-C000-000000000046}'
# On Sat Sep 12 14:27:46 2026
'Microsoft Visio 16.0 Type Library'
makepy_version = '0.5.01'
python_version = 0x30b05f0

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{00021A98-0000-0000-C000-000000000046}')
MajorVersion = 4
MinorVersion = 16
LibraryFlags = 8
LCID = 0x0

class EDocument:
	'Visio Document Event Interface'
	CLSID = CLSID_Sink = IID('{000D0750-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{00021A21-0000-0000-C000-000000000046}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		        2 : "OnDocumentOpened",
		        1 : "OnDocumentCreated",
		        3 : "OnDocumentSaved",
		        4 : "OnDocumentSavedAs",
		     8194 : "OnDocumentChanged",
		    16386 : "OnBeforeDocumentClose",
		    32772 : "OnStyleAdded",
		     8196 : "OnStyleChanged",
		    16388 : "OnBeforeStyleDelete",
		    32776 : "OnMasterAdded",
		     8200 : "OnMasterChanged",
		    16392 : "OnBeforeMasterDelete",
		    32784 : "OnPageAdded",
		     8208 : "OnPageChanged",
		    16400 : "OnBeforePageDelete",
		    32832 : "OnShapeAdded",
		      901 : "OnBeforeSelectionDelete",
		        5 : "OnRunModeEntered",
		        6 : "OnDesignModeEntered",
		        7 : "OnBeforeDocumentSave",
		        8 : "OnBeforeDocumentSaveAs",
		        9 : "OnQueryCancelDocumentClose",
		       10 : "OnDocumentCloseCanceled",
		      300 : "OnQueryCancelStyleDelete",
		      301 : "OnStyleDeleteCanceled",
		      400 : "OnQueryCancelMasterDelete",
		      401 : "OnMasterDeleteCanceled",
		      500 : "OnQueryCancelPageDelete",
		      501 : "OnPageDeleteCanceled",
		      802 : "OnShapeParentChanged",
		      803 : "OnBeforeShapeTextEdit",
		      804 : "OnShapeExitedTextEdit",
		      903 : "OnQueryCancelSelectionDelete",
		      904 : "OnSelectionDeleteCanceled",
		      905 : "OnQueryCancelUngroup",
		      906 : "OnUngroupCanceled",
		      907 : "OnQueryCancelConvertToGroup",
		      908 : "OnConvertToGroupCanceled",
		      909 : "OnQueryCancelGroup",
		      910 : "OnGroupCanceled",
		      807 : "OnShapeDataGraphicChanged",
		    16416 : "OnBeforeDataRecordsetDelete",
		    32800 : "OnDataRecordsetAdded",
		       11 : "OnAfterRemoveHiddenInformation",
		       13 : "OnRuleSetValidated",
		       14 : "OnAfterDocumentMerge",
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:
#	def OnDocumentOpened(self, doc=defaultNamedNotOptArg):
#	def OnDocumentCreated(self, doc=defaultNamedNotOptArg):
#	def OnDocumentSaved(self, doc=defaultNamedNotOptArg):
#	def OnDocumentSavedAs(self, doc=defaultNamedNotOptArg):
#	def OnDocumentChanged(self, doc=defaultNamedNotOptArg):
#	def OnBeforeDocumentClose(self, doc=defaultNamedNotOptArg):
#	def OnStyleAdded(self, Style=defaultNamedNotOptArg):
#	def OnStyleChanged(self, Style=defaultNamedNotOptArg):
#	def OnBeforeStyleDelete(self, Style=defaultNamedNotOptArg):
#	def OnMasterAdded(self, Master=defaultNamedNotOptArg):
#	def OnMasterChanged(self, Master=defaultNamedNotOptArg):
#	def OnBeforeMasterDelete(self, Master=defaultNamedNotOptArg):
#	def OnPageAdded(self, Page=defaultNamedNotOptArg):
#	def OnPageChanged(self, Page=defaultNamedNotOptArg):
#	def OnBeforePageDelete(self, Page=defaultNamedNotOptArg):
#	def OnShapeAdded(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeSelectionDelete(self, Selection=defaultNamedNotOptArg):
#	def OnRunModeEntered(self, doc=defaultNamedNotOptArg):
#	def OnDesignModeEntered(self, doc=defaultNamedNotOptArg):
#	def OnBeforeDocumentSave(self, doc=defaultNamedNotOptArg):
#	def OnBeforeDocumentSaveAs(self, doc=defaultNamedNotOptArg):
#	def OnQueryCancelDocumentClose(self, doc=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel close of document? T:Yes F:No'
#	def OnDocumentCloseCanceled(self, doc=defaultNamedNotOptArg):
#		'Document close operation was canceled.'
#	def OnQueryCancelStyleDelete(self, Style=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of style? T:Yes F:No'
#	def OnStyleDeleteCanceled(self, Style=defaultNamedNotOptArg):
#		'Delete style operation was canceled.'
#	def OnQueryCancelMasterDelete(self, Master=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of master? T:Yes F:No'
#	def OnMasterDeleteCanceled(self, Master=defaultNamedNotOptArg):
#		'Delete master operation was canceled.'
#	def OnQueryCancelPageDelete(self, Page=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of page? T:Yes F:No'
#	def OnPageDeleteCanceled(self, Page=defaultNamedNotOptArg):
#		'Delete page operation was canceled.'
#	def OnShapeParentChanged(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeShapeTextEdit(self, Shape=defaultNamedNotOptArg):
#	def OnShapeExitedTextEdit(self, Shape=defaultNamedNotOptArg):
#	def OnQueryCancelSelectionDelete(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel delete of shapes? T:Yes F:No'
#	def OnSelectionDeleteCanceled(self, Selection=defaultNamedNotOptArg):
#		'Delete shapes operation was canceled.'
#	def OnQueryCancelUngroup(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel ungroup operation? T:Yes F:No'
#	def OnUngroupCanceled(self, Selection=defaultNamedNotOptArg):
#		'Ungroup operation was canceled.'
#	def OnQueryCancelConvertToGroup(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel convert to group operation? T:Yes F:No'
#	def OnConvertToGroupCanceled(self, Selection=defaultNamedNotOptArg):
#		'Convert to group operation was canceled.'
#	def OnQueryCancelGroup(self, Selection=defaultNamedNotOptArg, lpboolRet=pythoncom.Missing):
#		'Cancel group operation? T:Yes F:No'
#	def OnGroupCanceled(self, Selection=defaultNamedNotOptArg):
#		'Group operation was canceled.'
#	def OnShapeDataGraphicChanged(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeDataRecordsetDelete(self, DataRecordset=defaultNamedNotOptArg):
#	def OnDataRecordsetAdded(self, DataRecordset=defaultNamedNotOptArg):
#	def OnAfterRemoveHiddenInformation(self, doc=defaultNamedNotOptArg):
#	def OnRuleSetValidated(self, RuleSet=defaultNamedNotOptArg):
#	def OnAfterDocumentMerge(self, coauthMergeObjects=defaultNamedNotOptArg):


win32com.client.CLSIDToClass.RegisterCLSID( "{000D0750-0000-0000-C000-000000000046}", EDocument )
