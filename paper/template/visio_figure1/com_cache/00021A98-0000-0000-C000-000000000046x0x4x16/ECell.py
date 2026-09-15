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

class ECell:
	'Visio Cell Event Interface'
	CLSID = CLSID_Sink = IID('{000D0B0D-0000-0000-C000-000000000046}')
	coclass_clsid = IID('{000D0A0D-0000-0000-C000-000000000046}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		    10240 : "OnCellChanged",
		    12288 : "OnFormulaChanged",
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
#	def OnFormulaChanged(self, Cell=defaultNamedNotOptArg):
#		"Fires after a cell's formula changes."


win32com.client.CLSIDToClass.RegisterCLSID( "{000D0B0D-0000-0000-C000-000000000046}", ECell )
