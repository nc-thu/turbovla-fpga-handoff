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

class EShape:
	'Visio Shape Event Interface'
	CLSID = CLSID_Sink = IID('{000D0B0B-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A0A-0000-0000-C000-000000000046}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		    10240 : "OnCellChanged",
		    32832 : "OnShapeAdded",
		      901 : "OnBeforeSelectionDelete",
		     8256 : "OnShapeChanged",
		      902 : "OnSelectionAdded",
		    16448 : "OnBeforeShapeDelete",
		     8320 : "OnTextChanged",
		    12288 : "OnFormulaChanged",
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
		      805 : "OnShapeLinkAdded",
		      806 : "OnShapeLinkDeleted",
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
#	def OnCellChanged(self, Cell=defaultNamedNotOptArg):
#		"Fires after a cell's value changes."
#	def OnShapeAdded(self, Shape=defaultNamedNotOptArg):
#	def OnBeforeSelectionDelete(self, Selection=defaultNamedNotOptArg):
#	def OnShapeChanged(self, Shape=defaultNamedNotOptArg):
#	def OnSelectionAdded(self, Selection=defaultNamedNotOptArg):
#	def OnBeforeShapeDelete(self, Shape=defaultNamedNotOptArg):
#	def OnTextChanged(self, Shape=defaultNamedNotOptArg):
#	def OnFormulaChanged(self, Cell=defaultNamedNotOptArg):
#		"Fires after a cell's formula changes."
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
#	def OnShapeLinkAdded(self, Shape=defaultNamedNotOptArg, DataRecordsetID=defaultNamedNotOptArg, DataRowID=defaultNamedNotOptArg):
#	def OnShapeLinkDeleted(self, Shape=defaultNamedNotOptArg, DataRecordsetID=defaultNamedNotOptArg, DataRowID=defaultNamedNotOptArg):


win32com.client.CLSIDToClass.RegisterCLSID( "{000D0B0B-0000-0000-C000-000000000046}", EShape )
